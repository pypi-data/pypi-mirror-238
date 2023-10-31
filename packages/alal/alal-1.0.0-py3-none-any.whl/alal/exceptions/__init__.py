from .exceptions import *

exception_class = {
    500: AlalServerErrors,
    404: AlalNotFound,
    400: AlalBadRequest,
    401: AlalUnauthorized
}