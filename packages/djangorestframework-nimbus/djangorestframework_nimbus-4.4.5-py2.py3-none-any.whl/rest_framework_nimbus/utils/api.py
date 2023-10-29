# -*- coding: utf-8 -*-
import re
import uuid
from dateutil import parser
from datetime import datetime
import logging
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db.models.signals import class_prepared
from django.forms.models import model_to_dict, fields_for_model, ALL_FIELDS
from django.urls import reverse
from django.shortcuts import resolve_url
from django.core import validators
from django.utils import timezone
from django.utils import dateformat
from django.utils.timezone import make_aware, make_naive, is_aware, is_naive, now, utc
from django.utils.encoding import smart_str, smart_bytes
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import uuid

__all__ = [
    "get_client_ip",
    "to_python_boolean",
    "within_time_range",
    "get_queryparam",
    "get_header",
    "get_data",
    "to_datetime",
    "get_uid",
]


logger = logging.getLogger(__name__)


def get_client_ip(request):
    """
    get client ip from request Meta

    :param request:request
    :return: ip
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', '')
    return ip


def to_python_boolean(string):
    """Convert a string to boolean.

    :param string: type: str
    """
    string = string.lower()
    if string in ('t', 'true', '1'):
        return True
    if string in ('f', 'false', '0'):
        return False
    raise ValueError("Invalid boolean value: '%s'" % string)


def within_time_range(d1, d2, maxdiff_seconds):
    '''Return true if two datetime.datetime object differs less than the given seconds'''
    delta = d2 - d1 if d2 > d1 else d1 - d2
    # delta.total_seconds() is only available in python 2.7+
    diff = (delta.microseconds + (delta.seconds + delta.days*24*3600) * 1e6) / 1e6
    return diff < maxdiff_seconds


def get_queryparam(request, keyword, default=None):
    """
    get query param from request.post data

    :param request: request
    :param keyword: keyword
    :param default: default:None
    :return: value
    """
    value = request.GET.get(keyword, default)
    return value or request.POST.get(keyword, default)


def get_header(request, key, default=None):
    """
    get the head of request.Meta

    :param request: request
    :param key: key
    :param default: default:None
    :return: value
    """
    key = u"HTTP_{}".format(key).upper()
    return request.META.get(key, default)


def get_data(request, key, default=None):
    """
    get data from request.data

    :param request: request
    :param key: key
    :param default: default:None
    :return: value
    """
    return request.data.get(key, default)


def to_datetime(timestamp):
    """
    Time stamp into time; type:datetime

    :param timestamp:time stamp
    :return: datetime
    """
    try:
        return datetime.fromtimestamp(timestamp, timezone.get_current_timezone())
    except Exception as e:
        logger.error(e)
    try:
        return parser.parse(timestamp)
    except Exception as e:
        logger.error(e)
    return None


def get_uid():
    """
    Get random uuid

    :return: uuid
    """
    return uuid.uuid4().hex
