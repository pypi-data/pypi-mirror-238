# Django
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third party
from ckeditor_uploader.fields import RichTextUploadingField
from cms.models.pluginmodel import CMSPlugin
from filer.fields.file import FilerFileField

# Local application / specific library imports
from .conf.settings import SIMPLE_NOTES_APP_NAME, SIMPLE_NOTES_NOTE_ADMIN_NAME


class SimpleNote(CMSPlugin):
    note = RichTextUploadingField(blank=True, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    language_code = models.CharField(max_length=5, default="")
    categories = models.ManyToManyField(to="Category", related_name="notes", blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=128, verbose_name=_("Author"))
    site = models.ForeignKey(
        Site, null=True, blank=True, on_delete=models.PROTECT, editable=False
    )

    def __str__(self):
        return f"{self.content_object}"

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        verbose_name = SIMPLE_NOTES_NOTE_ADMIN_NAME
        verbose_name_plural = SIMPLE_NOTES_APP_NAME


class SimpleFile(models.Model):
    note = models.ForeignKey(SimpleNote, on_delete=models.CASCADE)
    file = FilerFileField(
        null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=("Files")
    )

    def __str__(self):
        return ""

    class Meta:
        verbose_name = _("Extra file")
        verbose_name_plural = _("Extra files")


class Category(models.Model):
    label = models.CharField(_("Category"), max_length=512)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return f"{self.label}"
