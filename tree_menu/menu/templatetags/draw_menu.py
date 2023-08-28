from django import template
from ..models import Section


register = template.Library()


@register.inclusion_tag("menu/main_menu.html", takes_context=True)
def draw_menu(context, menu_name):
    """
    Функция возвращает корневой объект со всеми его потомками, сохраненными
    в отдельном атрибуте. Каждый последующий потомок имеет атрибут с его
    потомками на глубину выбранного на странице объекта(берётся из контекста).
    """
    menu = Section.objects.filter(menu__title=menu_name)
    m = [(entry.parent_id, entry.id) for entry in menu]
    menu = [i for i in menu]
    child_dict = {}
    for key, value in m:
        if child_dict.get(key, False) is False:
            child_dict[key] = [value]
        else:
            child_dict[key].append(value)
    try:
        name = context["name"]
        if menu[0].menu.title == name:
            selected = context["section_pk"]
        else:
            selected = None
    except KeyError:
        selected = None

    select_list = selected_list(child_dict, selected)
    print(select_list)
    menu = get_menu(menu, select_list)
    # print(menu)
    return {"menu": menu}


def selected_list(child_list, selected):
    """
    Функция для определения списка всех потомков до выбранного объекта
    включительно.
    :param child_list: Список всех потомков относительно выбранного меню.
    :param selected: Выбранный объект на странице.
    :return: Список из предков, предшествующим выбранному объекту.
    """
    if selected is None:
        return child_list[None]
    result = [selected]
    temp = selected
    while temp:
        for parent, kids in child_list.items():
            if temp in kids:
                temp = parent
                result.append(temp)
    return result


def get_menu(menu, select_list):
    """
    Функция для получения всех необходимых элементов меню.
    :param menu: Список всех вершин меню
    :param select_list: Список вершин-предков
    :return: Список содержащий один корневой объект со всеми его потомками.
    """
    menu = menu.copy()
    for i in menu:
        i.kids = []
        if i.id in select_list:
            for j in menu:
                if j.parent_id == i.id:
                    i.kids.append(j)
    return [menu[0]]
