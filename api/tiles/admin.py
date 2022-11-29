from django.contrib import admin
from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreeNodeForm


from .models import KMLMapAsset, LayerFolder, MapLayer, KMLMap


@admin.register(MapLayer)
class MapLayerAdmin(admin.ModelAdmin):
    model = MapLayer
    list_display = ['label', 'slug', 'tiles_url',
                    'get_has_tiles', 'depth']

    def get_has_tiles(self, obj):
        return obj.has_tiles()
    get_has_tiles.boolean = True
    get_has_tiles.short_description = "Tuiles"


class KMLMapAssetInline(admin.TabularInline):
    model = KMLMapAsset


@admin.register(KMLMap)
class KMLMapAdmin(admin.ModelAdmin):
    model = KMLMap
    list_display = ['label']
    inlines = [KMLMapAssetInline]


@admin.register(LayerFolder)
class LayerFolderAdmin(TreeNodeModelAdmin):
    treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
    #treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
    # treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_BREADCRUMBS
    # treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_INDENTATION
    form = TreeNodeForm
    filter_horizontal = ['layers']
    list_display = ['get_layers']
    model = LayerFolder

    def get_layers(self, obj):
        return ", ".join(obj.layers.values_list('label', flat=True).all())
    get_layers.short_description = "Calques"
