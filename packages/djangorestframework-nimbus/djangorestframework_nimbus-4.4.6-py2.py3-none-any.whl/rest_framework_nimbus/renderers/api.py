# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging
import six
from django.conf import settings
from rest_framework import status
from rest_framework import renderers
from rest_framework.utils import encoders
from rest_framework_nimbus.settings import api_settings
from rest_framework_nimbus.handler import api_render_data, api_exception_data
from .base import JSONRenderer, BaseAPIRenderer

logger = logging.getLogger(__name__)


class APIRenderer(BaseAPIRenderer):
    def get_api_data(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "code": status_code,
            "status": "SUCCESS",
            "errorCode": None,
            "detailMessages": None,
            "responseBody": data
        }
        if not str(status_code).startswith('2'):
            response["status"] = "ERROR"
            response["responseBody"] = None
            try:
                err_code, err_detail = self._get_exception_info(ex=data, default_code=status_code)
                response["errorCode"] = err_code
                response["detailMessages"] = err_detail
            except KeyError:
                logger.error(data)
                response["responseBody"] = data
        return response

    def _get_exception_info(self, ex, default_code=status.HTTP_400_BAD_REQUEST):
        logger.error(ex)
        if isinstance(ex, dict):
            err = ex.get("detail", "")
        elif isinstance(ex, six.string_types):
            err = ex
        if isinstance(err, dict):
            err_code = err.get("code", default_code)
        else:
            err_code = getattr(err, "code", default_code)
        if isinstance(err, dict):
            err_detail = err.get("detail", err)
        else:
            err_detail = getattr(err, "detail", err)
        if not err_detail and settings.DEBUG:
            err_detail = str(ex)
        return err_code, err_detail


class APIVueRenderer(BaseAPIRenderer):
    def get_api_data(self, data, accepted_media_type=None, renderer_context=None):
        return api_render_data(data=data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)