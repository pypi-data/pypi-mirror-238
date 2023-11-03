import os
import uuid

from django.contrib.admin.models import ADDITION, CHANGE, LogEntry
from django.contrib.admin.utils import construct_change_message
from django.contrib.contenttypes.models import ContentType


def get_private_file_path(instance, filename):

    filename, file_extension = os.path.splitext(filename)
    path = str(instance._meta).replace('.', '/')
    filename = '%s%s' % (str(uuid.uuid4()), file_extension)
    return os.path.join(path, filename)


def create_log_entry(user_id, obj, new, form=None, msg=None):
    """Creates a Log Entry in the Django Admin History"""

    change_message = msg if msg is not None else construct_change_message(form, None, True if new else False)
    if user_id is None:
        user_id = 1  # Default System User

    LogEntry.objects.log_action(
        user_id,
        ContentType.objects.get_for_model(obj.__class__).id,
        obj.id,
        str(obj),
        ADDITION if new else CHANGE,
        change_message
    )
