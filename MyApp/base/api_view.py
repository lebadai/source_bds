import datetime
import json
from django.utils import translation
from django.core.paginator import Paginator, EmptyPage
from library.functions import datetime_to_string
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status, exceptions
from library.constant.error_codes import ERROR_CODE_MESSAGE
from library.constant.api import SERVICE_MESSAGE
from MyProject.settings import DATETIME_OUTPUT_FORMATS
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from library.constant.language import LANGUAGES_TO_ID, LANGUAGE_TYPE_VIETNAMESE, ID_TO_LANGUAGES
from library.constant.api import PAGINATOR_PER_PAGE, SORT_TYPE_TO_ID, ORDER_BY_DESC
from MyProject.settings import DEFAULT_LANGUAGE_ID
from MyApp.base.exception import CustomAPIException


class DjangoOverRideJSONEncoder(DjangoJSONEncoder):
    """
    JSONEncoder subclass that knows how to encode/time and decimal types.
    """

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = datetime_to_string(o, DATETIME_OUTPUT_FORMATS)
            return r
        else:
            return super(DjangoOverRideJSONEncoder, self).default(o)


class BinaryFileRenderer(BaseRenderer):
    media_type = 'application/octet-stream'
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class CustomAPIView(GenericViewSet):
    authentication_classes = (IsAuthenticatedOrReadOnly,)
    permission_classes = ()
    renderer_classes = (BinaryFileRenderer,)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.is_paging = False
        self.total_page = None
        self.total_record = None
        self.per_page = PAGINATOR_PER_PAGE
        self.page = 1
        self.paging_list = None
        self.current_page = None
        self.sort = ORDER_BY_DESC  # default sort via children by desc
        self.lang = DEFAULT_LANGUAGE_ID
        self.lang_code = ID_TO_LANGUAGES[DEFAULT_LANGUAGE_ID]
        self.order_by = 'id'

    def dispatch(self, *args, **kwargs):
        response = super(CustomAPIView, self).dispatch(*args, **kwargs)

        # if LOGGER_PRINT:
        #     # logger.info(response.data)
        #
        #     from django.db import connection
        #     for query in connection.queries:
        #         logger.debug(f"\n{query['sql']}")
        #         logger.debug(f"\n{query['time']}")
        #
        #     logger.info(f"Total number of queries = {len(connection.queries)}")
        #     logger.success("Query Complete!")

        return response

    def initial(self, request, *args, **kwargs):
        self.renderer_classes = (JSONRenderer,)
        self.parse_common_params(request)
        translation.activate(self.lang_code)

    def parse_common_params(self, request):
        self.lang_code = request.META.get('HTTP_MNV_LANGUAGE', ID_TO_LANGUAGES.get(LANGUAGE_TYPE_VIETNAMESE))
        self.lang = LANGUAGES_TO_ID.get(self.lang_code, LANGUAGE_TYPE_VIETNAMESE)
        self.sort = SORT_TYPE_TO_ID.get(request.GET.get('sort', 'desc'), ORDER_BY_DESC)

        per_page = self.request.query_params.get('limit', None)
        if per_page and per_page.isdigit():
            self.per_page = int(per_page)

        page = self.request.query_params.get('page', None)
        if page and page.isdigit():
            self.page = int(page)

        # TODO: fix it, input values list
        order_by = self.request.query_params.get('order_by', None)
        if type(order_by) is list:
            order_by = ",".join(map(str, self.order_by))
        if order_by and isinstance(order_by, str):
            self.order_by = order_by

    def paginate(self, query_set):
        is_order = getattr(query_set, 'ordered', None)
        if not is_order:
            query_set = query_set.order_by(self.order_by)

        paginator = Paginator(query_set, per_page=self.per_page)

        self.total_record = paginator.count
        self.total_page = paginator.num_pages
        self.is_paging = True
        try:
            self.paging_list = list(paginator.page(self.page))
        except EmptyPage:
            self.paging_list = []

    def response_delete(self, total_items=1, total_deleted=1):
        result = {
            'success': True,
            'detail': {
                'total_items': total_items,
                'total_deleted': total_deleted,
            },
        }
        return result   

    @staticmethod
    def _response(data, status_code=status.HTTP_200_OK):
        return Response(json.loads(json.dumps(data, cls=DjangoOverRideJSONEncoder)), status=status_code)

    def response_paging(self, data):
        if not (isinstance(data, list) or isinstance(data, dict)):
            raise exceptions.ParseError('data must be dict or list')

        return self._response({
            'items': data,
            'total_page': self.total_page,
            'total_record': len(data) if not self.is_paging and isinstance(data, list) else self.total_record,
            'page': self.page,
        })

    def response_success(self, data, status_code=status.HTTP_200_OK):
        return self._response(data, status_code)

    def http_exception(self, error_code=None, description=None, status_code=status.HTTP_400_BAD_REQUEST):
        raise CustomAPIException(status_code=status_code, detail={
            'error_code': error_code,
            'description': ERROR_CODE_MESSAGE.get(error_code, '') if not description else description
        })

    def check_key_content(self, key_content_list, check_key_list):
        list_key_missing = list()
        for key in check_key_list:
            if key not in key_content_list:
                list_key_missing.append(key)
        if len(list_key_missing) > 0:
            return self.http_exception(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                description='Missing ' + ", ".join(list_key_missing)
            )

    def response(self, data): # noqa
        # if self.CLIENT_ENCODE:
        #     send_data = service_encode_from_json(data)
        # else:
        data = json.loads(json.dumps(data, cls=DjangoOverRideJSONEncoder))
        send_data = data
        # logger('------------Send Data-------------')
        # logger(send_data)
        res = Response(send_data)
        return res

    def response_exception(self, code, mess=None): # noqa
        if not mess:
            try:
                _mess = SERVICE_MESSAGE[code]
            except (ValueError, KeyError):
                _mess = ''
        else:
            _mess = mess
        fail = {'success': False, 'code': code, 'detail': _mess}
        raise exceptions.NotAcceptable(fail)

    def response_paging(self, data): # noqa
        if not (isinstance(data, list) or isinstance(data, dict)):
            raise exceptions.ParseError('data must be dict or list')

        result = {
            'success': True,
            'detail': data,
            'total_page': self.total_page,
            'total_record': self.total_record,
            'page': self.page,
        }
        if not self.is_paging:
            if isinstance(data, list):
                result['total_record'] = len(data)
        return result

    def validate_exception(self, text=None, code=None): # noqa
        fail = {
            'success': False,
            'detail': text,

        }
        raise exceptions.ValidationError(fail)

    def response_delete(self, total_items=1, total_deleted=1): # noqa
        result = {
            'success': True,
            'detail': {
                'total_items': total_items,
                'total_deleted': total_deleted,
            },
        }
        return result

    # def decode_to_json(self, data):
    #     if self.CLIENT_ENCODE:
    #         response = service_decode_to_json(data)
    #     else:
    #         response = json.loads(data)
    #     return response

    def response_success_permission(self, data, permission): # noqa
        result = {
            'success': True,
            'detail': data,
            'permission_flag': permission
        }
        return result

    def response_paging(self, data):
        if not (isinstance(data, list) or isinstance(data, dict)):
            raise exceptions.ParseError('data must be dict or list')

        result = {
            'success': True,
            'detail': data,
            'total_page': self.total_page,
            'total_record': self.total_record,
            'page': self.page,
        }
        if not self.is_paging:
            if isinstance(data, list):
                result['total_record'] = len(data)
        return result


