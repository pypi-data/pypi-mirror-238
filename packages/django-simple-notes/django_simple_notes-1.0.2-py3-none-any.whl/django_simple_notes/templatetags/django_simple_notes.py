# Django
from django import template
from django.contrib.auth.models import Permission
from django.db.models import Q

# Project
from django_simple_notes.cms_toolbars import get_content_type_and_id
from django_simple_notes.models import SimpleNote


def get_user_permissions(user):
    """Thx https://stackoverflow.com/a/27624324 for this method (useful for projects still in django 2.2)."""
    if user.is_superuser:
        return Permission.objects.all()
    if user.is_anonymous:
        return Permission.objects.none()
    return Permission.objects.filter(
        Q(group__in=user.groups.all()) | Q(user=user)
    ).distinct()


register = template.Library()


@register.simple_tag(takes_context=True)
def get_non_empty_note(context, *args, **kwargs):
    # we might not have a user in our context so handle the case
    permission_to_see_notes = False
    try:  # noqa: FURB107
        # check perm to see notes
        permission_to_see_notes = (
            get_user_permissions(context["user"])
            .filter(codename="view_simplenote")
            .exists()
        )
    except KeyError:
        pass
    if not permission_to_see_notes:
        return False

    # if you can see notes, then search for the note content
    ct, id = get_content_type_and_id(context["request"])
    try:
        note = SimpleNote.objects.get(  # noqa
            ~Q(note__exact=""),
            ~Q(note__exact=None),
            content_type=ct,
            object_id=id,
            language_code=context["request"].LANGUAGE_CODE,
        )
        return note
    except SimpleNote.DoesNotExist:
        pass
    return False
