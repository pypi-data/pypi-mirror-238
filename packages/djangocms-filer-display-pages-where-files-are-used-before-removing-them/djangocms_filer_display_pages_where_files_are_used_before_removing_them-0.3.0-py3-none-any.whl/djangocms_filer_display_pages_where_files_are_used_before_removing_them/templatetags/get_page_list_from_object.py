from django import template
from django.utils.translation import gettext_lazy as _
from djangocms_file.models import File
from djangocms_picture.models import Picture


register = template.Library()


def get_page_list_from_object(obj):
    pages_list = []

    not_on_a_page_str = _("Not on a page (plugin id only)")

    # Picture
    if str(type(obj)) == "<class 'filer.models.imagemodels.Image'>":
        pictures = Picture.objects.filter(picture=obj)
        for plugin in pictures:
            page = plugin.placeholder.page
            if page is None:
                page = plugin.page
            if page is None:
                pages_list.append(
                    {
                        "file_name": plugin.picture.original_filename,
                        "url": None,
                        "title": f"{not_on_a_page_str} {plugin.id})",
                        "is_draft": False,
                        "lang": plugin.language,
                    }
                )
            else:
                pages_list.append(
                    {
                        "file_name": plugin.picture.original_filename,
                        "url": page.get_absolute_url(plugin.language),
                        "title": page.get_page_title(plugin.language),
                        "is_draft": page.publisher_is_draft,
                        "lang": plugin.language,
                    }
                )
    # File
    elif str(type(obj)) == "<class 'filer.models.filemodels.File'>":
        files = File.objects.filter(file_src=obj)
        for plugin in files:
            page = plugin.placeholder.page
            if page is None:
                page = plugin.page
            if page is None:
                pages_list.append(
                    {
                        "file_name": plugin.file_src.original_filename,
                        "url": None,
                        "title": f"{not_on_a_page_str} {plugin.id})",
                        "is_draft": False,
                        "lang": plugin.language,
                    }
                )
            else:
                pages_list.append(
                    {
                        "file_name": plugin.file_src.original_filename,
                        "url": page.get_absolute_url(plugin.language),
                        "title": page.get_page_title(plugin.language),
                        "is_draft": page.publisher_is_draft,
                        "lang": plugin.language,
                    }
                )

    return pages_list


def get_files_from_folder(folder):
    childrens = folder.children.all()
    if childrens.exists():
        for child_folder in folder.children.all():
            return list(folder.files) + list(get_files_from_folder(child_folder))
    else:
        return list(folder.files)


def get_page_list_from_folder_and_files(folders, files):
    # lots of empty lists
    pages_list = []
    files_list = []

    # get files in every deleted folder
    for folder in folders:
        files_list += get_files_from_folder(folder)

    # add deleted files to the list
    for file in files:
        files_list.append(file)

    # find page for each file
    for file in files_list:
        pages_list.extend(get_page_list_from_object(file))

    return pages_list


register.filter(
    "get_page_list_from_folder_and_files", get_page_list_from_folder_and_files
)
register.filter("get_page_list_from_object", get_page_list_from_object)
