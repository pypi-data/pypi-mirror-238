# -*- coding: utf-8 -*-
import logging
from django.conf import settings
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework_nimbus.err_code import ErrCode, APIError
from rest_framework_nimbus.exceptions import APIException


logger = logging.getLogger(__name__)


def api_render_data(data, accepted_media_type=None, renderer_context=None, **kwargs):
    status_code = str(renderer_context['response'].status_code)
    response = {
        "code": ErrCode.SUCCESS.code,
    }
    if not status_code.startswith('2'):
        response["code"] = ErrCode.ERROR.code
        response["message"] = ErrCode.ERROR.message
        try:
            err_code, err_detail = _get_exception_info(ex=data, default_code=status_code)
            if err_code:
                response["code"] = err_code
            response["detail"] = err_detail
        except KeyError:
            logger.error(data)
            response["code"] = ErrCode.ERROR.code
            response["message"] = ErrCode.ERROR.message
            response["detail"] = data
    else:
        response["detail"] = ""
        response["message"] = "SUCCESS"
        response["data"] = data
    return response


def api_exception_data(exc, context=None, **kwargs):
    logger.exception(exc)
    status_code = getattr(exc, "status_code", status.HTTP_400_BAD_REQUEST)
    code = str(ErrCode.ERROR)
    response = {
        "code": code,
        "message": "ERROR",
        "data": "",
        "detail": "",
    }
    err_code, err_detail = _get_exception_info(ex=exc, default_code=code)
    if err_code:
        response["code"] = err_code
    response["detail"] = err_detail
    return Response(response, status=status_code)


def _get_exception_info(ex, default_code=status.HTTP_400_BAD_REQUEST):
    logger.error(ex)
    if isinstance(ex, APIError):
        detail = ex.get_res_dict()
        err_code = detail.code
        err_detail = detail.message
        return err_code, err_detail
    if isinstance(ex, APIException):
        err_code = ex.code
        err_detail = ex.detail
        return err_code, err_detail
    if isinstance(ex, dict):
        err = ex.get("detail", "")
    elif isinstance(ex, str):
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
    return str(ErrCode.ERROR), err_detail

