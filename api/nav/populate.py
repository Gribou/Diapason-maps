

from .models import Shortcut, ToolbarItem

DEFAULT_SHORTCUTS = [
    {'label': 'Téléphones', 'category': 'PHONE', 'url': "/telephones"},
    {"label": "Fichiers", 'category': 'FILE', 'url': "/files"},
    {"label": "CIV", 'category': 'SCHEDULE', "url": "/civ"},
    {"label": "Carte", 'category': 'MAP', 'url': "/map"}
]

DEFAULT_TOOLBAR = ['/civ', '/map']


def populate(verbose=False):
    if not Shortcut.objects.exists():
        for shortcut in DEFAULT_SHORTCUTS:
            Shortcut.objects.create(**shortcut)
            if verbose:
                print("Raccourci {} créé".format(shortcut['label']))

        for i, url in enumerate(DEFAULT_TOOLBAR):
            try:
                item = Shortcut.objects.get(url=url)
                ToolbarItem.objects.create(shortcut=item, rank=i)
                if verbose:
                    print("Elément de barre d'outils {} créé".format(item.label))
            except:
                pass
