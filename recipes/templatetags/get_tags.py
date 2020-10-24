from django import template

register = template.Library()


@register.filter
def get_tags(request, tag):
    tags = request.GET.get("tags", "")
    tags = tags.split(",") if tags else []
    if tag not in tags:
        tags.append(tag)
    else:
        tags.remove(tag)
    # print(tags)
    return ",".join(tags)
