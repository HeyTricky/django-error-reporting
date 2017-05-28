from utils import TypeSubRequest, OldFunctionToPatch
from models import Track, SubRequest, HttpRequest
import logging

old_func_to_patch = OldFunctionToPatch()


def patch_function(old_function, type_sub_request):
    def inner_patch_function(*args, **kwargs):
        message = "{0}: {1}".format(old_function.func_name.upper(), args[0])
        http_request = HttpRequest.objects.last()
        sub_request = SubRequest()
        sub_request.save_sub_request(http_request, type_sub_request, message)
        old_function(*args, **kwargs)

    return inner_patch_function


def start(request):
    request.first_request = True
    track = Track()
    track.save()
    print track
    request.session["is_reporting"] = track.id

    logging.debug = patch_function(logging.debug, TypeSubRequest.LOG)
    logging.info = patch_function(logging.info, TypeSubRequest.LOG)
    logging.critical = patch_function(logging.critical, TypeSubRequest.LOG)
    logging.error = patch_function(logging.error, TypeSubRequest.LOG)
    logging.exception = patch_function(logging.exception, TypeSubRequest.LOG)

    # [patch_function(func_to_patch, TypeSubRequest.LOG) for func_to_patch in LOG_FUNCTIONS_TO_PATCH]
    # for j in range(len(LOG_FUNCTIONS_TO_PATCH)):
    #    LOG_FUNCTIONS_TO_PATCH[j] = patch_function(LOG_FUNCTIONS_TO_PATCH[j], TypeSubRequest.LOG)
    # for func_to_patch in LOG_FUNCTIONS_TO_PATCH:
    #    func_to_patch = patch_function(func_to_patch, TypeSubRequest.LOG)


def stop(request):
    del request.session["is_reporting"]

    logging.debug = old_func_to_patch.debug
    logging.info = old_func_to_patch.info
    logging.critical = old_func_to_patch.critical
    logging.error = old_func_to_patch.error
    logging.exception = old_func_to_patch.exception


def generate_report():
    pass
