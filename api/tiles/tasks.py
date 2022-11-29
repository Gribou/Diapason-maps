from celery import shared_task
from django.core.files.storage import default_storage
from mbutil import mbtiles_to_disk
from zipfile import ZipFile
from django.apps import apps
import os
import json
import shutil


def _get_layer_model():
    return apps.get_model(app_label="tiles", model_name="MapLayer")


def prepare_layer(layer_pk):
    layer = _get_layer_model().objects.filter(pk=layer_pk).first()
    if layer is None:
        raise ValueError("No MapLayer with this id : {}".format(layer_pk))
    try:
        # create tiles folder if does not exist
        os.mkdir(default_storage.path("tiles"))
    except:
        pass
    destination_folder = os.path.join("tiles", layer.slug)
    # delete previously generated tiles
    if default_storage.exists(destination_folder):
        shutil.rmtree(default_storage.path(destination_folder))
    return layer, destination_folder


def parse_metadata_file(destination_folder):
    with default_storage.open(
            os.path.join(destination_folder, "metadata.json")) as f:
        return json.load(f)


@shared_task
def make_tiles_from_mbtiles(layer_pk):
    layer, destination_folder = prepare_layer(layer_pk)
    source_file = layer.mbtiles_file.path
    # generate new tiles
    try:
        mbtiles_to_disk(source_file, default_storage.path(
            destination_folder), scheme="xyz")
        # save metadata into models
        layer.metadata = parse_metadata_file(destination_folder)
    finally:
        # delete source file
        os.remove(source_file)
        layer.mbtiles_file = None
        layer.save()


@shared_task
def make_tiles_from_zip(layer_pk):
    layer, destination_folder = prepare_layer(layer_pk)
    source_file = layer.zip_file.path
    # generate new tiles
    try:
        with ZipFile(source_file, 'r') as zip_obj:
            zip_obj.extractall(default_storage.path(destination_folder))
        if default_storage.exists(
                os.path.join(default_storage.path(destination_folder), "metadata.json")):
            layer.metadata = parse_metadata_file(destination_folder)
        else:
            # generate metadata from available files
            zoomlevels = [int(d) for d in default_storage.listdir(
                destination_folder)[0] if d.isnumeric()]
            if zoomlevels:
                first_file = get_first_file(destination_folder)
                layer.metadata = {
                    'minzoom': min(zoomlevels),
                    'maxzoom': max(zoomlevels),
                    "format": first_file.split('.')[1] if first_file else None
                }
                # write to metadata.json
                with default_storage.open(os.path.join(destination_folder, "metadata.json"), 'w') as f:
                    json.dump(layer.metadata, f)
            else:
                layer.metadata = {
                    "error": "No zoom folder were found. Check that they are at the root of the zip file."
                }

    finally:
        # delete source file
        os.remove(source_file)
        layer.zip_file = None
        layer.save()


def walk_folder(root):
    folders, files = default_storage.listdir(root)
    for subfolder in folders:
        if subfolder == ".":
            continue
        new_base = os.path.join(root, subfolder)
        for f in walk_folder(new_base):
            yield f
    yield root, folders, files


def get_first_file(root):
    for _, _, files in walk_folder(root):
        if len(files) > 0:
            return files[0]
