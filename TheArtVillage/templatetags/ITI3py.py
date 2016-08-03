from django import template
from TheArtVillage.models import Art

register = template.Library()


@register.inclusion_tag('ArtVillage/filter.html')
def filter_art():

    all_cats = []

    cats = Art.objects.filter(authenticate__exact="approved")
    for cat in cats:
        if cat.category not in all_cats:
            all_cats += [cat.category]

    return {'cats': all_cats}


@register.inclusion_tag('ArtVillage/type.html')
def filter_type():

    all_types = []

    types = Art.objects.filter(authenticate__exact="approved")

    for t in types:
        if t.sub_category not in all_types:
            all_types += [t.sub_category]

    return {'types': all_types}

