import os


def delete_file_on_model_delete(sender, instance, **kwargs):
    ''' delete media file on model delete'''
    if instance.pdf:
        if os.path.isfile(instance.pdf.path):
            os.remove(instance.pdf.path)


def delete_old_file_on_model_update(sender, instance, **kwargs):
    ''' delete media file if updated'''
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).pdf
    except sender.DoesNotExist:
        return False
    new_file = instance.pdf
    if old_file and not old_file == new_file and os.path.isfile(old_file.path):
        os.remove(old_file.path)
