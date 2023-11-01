# django_simple_notes

Add private (available only to logged in users) notes to different pages of your Django-CMS site, through generic foreign keys (using content types).

<div align="center">
  <a href="https://gitlab.com/kapt/open-source/django-simple-notes/uploads/3347c5f7a59fc03ccdf085910ffe8ce3/django-simple-notes-demo.webm">
    <img src="https://gitlab.com/kapt/open-source/django-simple-notes/uploads/6627c1021ab019d79b984a6e54261525/image.png" alt="Demo video thumbnail" />
  </a>
</div>

<div align="center">
  <a href="https://pypi.org/project/django-simple-notes/">
    <img src="https://img.shields.io/pypi/v/django-simple-notes?color=%232a2" alt="icon pypi version" />
  </a>
  <a href="https://pypi.org/project/django-simple-notes/">
    <img src="https://img.shields.io/pypi/dm/django-simple-notes?color=%232a2" alt="icon pypi downloads" />
  </a>
</div>

# Requirements

- `django-filer`: manage media files using folders/permissions & a dedicated interface
- `django-ckeditor`: install version <6 if you're still on django<3
- `django-ckeditor-filebrowser-filer`: allow using django-filer filer system for image/file upload
- `django`: work with django 2.2+
- `python`: work with python >= 3.10 (may work with older versions of python 3)

# Install

- run `python3 -m pip install django_simple_notes`
  - *optional: add `django-ckeditor<6` if you're still using django < 3*
- add those apps to your `INSTALLED_APPS`:
  ```python
      "filer",
      "ckeditor",
      "ckeditor_uploader",  # for hosting images in your ckeditor view, see below for a ready-to-use config
      "ckeditor_filebrowser_filer",
      "django_simple_notes",
  ```
- config this ([see the doc here](https://django-ckeditor.readthedocs.io/en/latest/#required-for-using-widget-with-file-upload)):
  ```python
  CKEDITOR_UPLOAD_PATH = ""
  ```
- add those urls in your `urls.py`:
  ```python
      # Upload images using ckeditor & django-filer
      path('ckeditor/', include('ckeditor_uploader.urls')),
      path('filer/', include('filer.urls')),
      path('filebrowser_filer/', include('ckeditor_filebrowser_filer.urls')),
  ```
- run `python manage.py migrate django_simple_notes`
- that's all folks!

----

# Features

- Add private notes on nearly each page of your site
  - supports djangocms pages & djangocms-blog posts out of the box!
  - you *can* add your own function to support even more type of pages (in apphooks)!
  - privates notes contain 1 ckeditor field (you can add images inside it), and many file fields (if you need to store a particular pdf file for a page for example)
- Supports adding different notes for same page in different languages
- Single-site & multisite support!

----

# Templatetags, yay!

There's a templatetag you can use to display a text if a private note exists on the current page and is not empty. The templatetag will only return `True` if the current user is logged in and have the permission to view the private note.

Here's how to use it:

```jinja
{% load django_simple_notes %}

{% have_non_empty_note as check_have_non_empty_note %}
{% if check_have_non_empty_note %}
<p>
  <i>This page have a private note.</i>
</p>
{% endif %}
```

----

# How it works?

The main logic is in `cms_toolbars.py`, in the `get_content_type_and_id` function.

This function will try to retrieve the content type and the id of the object (CMS Page, DjangoCMS-blog Post...). If it find the object, another function will create an empty SimpleNote for this object, and will save it. This way, we don't need to differentiate the create and the edit link of the note in the toolbar (I don't know if it's possible to refresh only the toolbar to return the right link (create/edit)).

Another cool function is the `get_queryset` in `admin.py`. It will return the full queryset if we're on a `change` page (edit the object in the admin). It will however only returns the "non-empty" objects in the `list` view (in order to not clutter the list view too much).

----

# Customize it!

You can define your own function that find `object_ct` and `object_id` in your settings!

Django simple notes will try to get a function from your site settings, named `SIMPLE_NOTES_CUSTOM_CONTENT_TYPE_AND_ID`. It will then execute it, and if it returns `None, None` it will launch its own `get_content_type_and_id` function (in order to retrieve cms/djangocms-blog ct/id).

## Here's an example to get you started:

*Just copy/paste this file in your site settings, and update it to suits your needs.*

```py
def SIMPLE_NOTES_CUSTOM_CONTENT_TYPE_AND_ID(request):
    # init parameters
    object_ct = None
    object_id = None

    # condition from request (use this to find the object/page type)
    if request.resolver_match.view_name in (
        "my_app_view",
    ):
        # necessary imports, be sure to include them in your function or you might stumble accross an import loop
        from my_app.models import MyModel
        slug = (
            request.resolver_match.kwargs["slug"]
            if "slug" in request.resolver_match.kwargs
            else ""
        )

        # a condition (if we have a slug, then retrieve the object using its slug)
        if slug:
            my_object = MyModel.objects.get(slug=slug)
            object_ct = my_object
            object_id = my_object.id
        else:
            # another condition (for if we have its id)
            id = (
                request.resolver_match.kwargs["pk"]
                if "pk" in request.resolver_match.kwargs
                else ""
            )
            if id:
                my_object = MyModel.objects.get(id=id)
                object_ct = MyModel
                object_id = my_object.id

    # return found ct/id or None/None
    # None/None will allow the regular `get_content_type_and_id` to proceed, searching for cms or blog pages
    return object_ct, object_id
```

## In order to get the object url, you will need to add another function

This function is named `SIMPLE_NOTES_ADMIN_URLS`, and is called in `admin.py` if it exists.

It's goal is to return an url for the current object, in order to add a direct link to the page in the admin list view.

If the returned url is `None`, then simple notes will try to get the url of a CMS page or a djangocms-blog Post.

If no link is found, the object name will be displayed without a link.

*Here's an example to get you started:*

```py
def SIMPLE_NOTES_ADMIN_URLS(obj):
    if obj.content_type.model == "mymodel":  # an object from a model with get_absolute_url()
        from my_app.models import MyModel
        return MyModel.objects.get(id=obj.object_id).get_absolute_url()
    if obj.content_type.model == "myothermodel":  # another model, which don't have get_absolute_url()
        from django.urls import reverse
        return reverse("view-name", kwargs={"pk": obj.object_id})
    return None
```

## Oh, and you can customize this too:

* `SIMPLE_NOTES_TOOLBAR_MENU_TEXT` (Default to `_("Simple notes")`): The toolbar menu text.
* `SIMPLE_NOTES_TOOLBAR_EDIT_TEXT` (Default to `_("Edit note for current page")`): The toolbar edit button text.
* `SIMPLE_NOTES_TOOLBAR_LIST_TEXT` (Default to `_("Notes list")`): The toolbar "show list notes" text.
* `SIMPLE_NOTES_APP_NAME` (Default to `SIMPLE_NOTES_TOOLBAR_MENU_TEXT` content): App name in django admin.
* `SIMPLE_NOTES_NOTE_ADMIN_NAME` (Default to `_("note")`): Name of single object in django admin (used in title: "*Editing **note***").

![Toolbar screenshot](https://gitlab.com/kapt/open-source/django-simple-notes/uploads/b816124205dee0bc44799e03a1e291b4/image.png)
> *Toolbar screenshot with default values.*

## Ckeditor config

You will need to configure `django-ckeditor` in order to make it work in the notes. Here's a ready-to-use config snippet that you can paste on your project's settings:

```python
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_THUMBNAIL_SIZE = (150, 150)
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
  "default": {
    "language": "{{ language }}",
    "toolbar": "Simple",
    "toolbar_Simple": [
        ["Undo", "Redo"],
        ["Styles", "Format"],
        ["TextColor", "BGColor"],
        ["Subscript", "Superscript", "-", "RemoveFormat", "PasteText", "PasteFromWord", "FilerImage"],
        ["Link", "Unlink"],
        ["Source"],
    ],
    "autoParagraph": False,
    "colorButton_colors": "01b6ad,00b6ef,a0cd49,ffc01c,9d1a75,fff,000",
    "skin": "moono-lisa",
    "height": "600px",
    "extraPlugins": "filerimage",
    "removePlugins": "image"  # do not use the classic image plugin, use the one from django-ckeditor-filebrowser-filer
  }
}
```

*You can learn more about thoses config values and customize them values by having a look at the [django-ckeditor documentation](https://django-ckeditor.readthedocs.io/en/latest/#optional-customizing-ckeditor-editor).*

----

### Todo?

Here's a sneak peak of the (maybe) future features:

- supports simple django apps!
