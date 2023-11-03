from django.apps import apps
from django.template import Library
from django.utils.text import slugify

register = Library()

@register.simple_tag
def app_additional_config(app):
    """
    Get additional infos from the app config and build a second level menu
    """

    menu_icon = "ti ti-package"  # Default Icon
    menu_firstlevel = list()
    menu_secondlevel = list()
    app_config = apps.get_app_config(app['app_label'])

    # Menu icon
    if hasattr(app_config, 'menu_icon'):
        menu_icon = getattr(app_config, 'menu_icon')

    # Default Menu
    if not hasattr(app_config, 'menu_firstlvl') and not hasattr(app_config, 'menu_secondlvl'):
        menu_firstlevel = app['models']

    # First Level Menu
    if hasattr(app_config, 'menu_firstlvl'):
        for menu in getattr(app_config, 'menu_firstlvl'):
            for item in app['models']:
                if item['object_name'] in menu:
                    menu_firstlevel.append(item)

    # Second Lvl Menu
    if hasattr(app_config, 'menu_secondlvl'):
        for menu in getattr(app_config, 'menu_secondlvl'):
            menu_tmp = dict(name=menu[0], key=slugify(menu[0]), models=[])
            for item in app['models']:
                if item['object_name'] in menu[1]:
                    menu_tmp['models'].append(item)
            if len(menu_tmp['models']) > 0:
                menu_secondlevel.append(menu_tmp)

    return dict(
        menu_icon=menu_icon,
        menu_firstlevel=menu_firstlevel,
        menu_secondlevel=menu_secondlevel,
    )
