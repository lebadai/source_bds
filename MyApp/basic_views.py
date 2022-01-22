from rest_framework import HTTP_HEADER_ENCODING
from MyApp.base.api_view import CustomAPIView


class BaseAPIView(CustomAPIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        # self.payment_policy = request.payment_policy
    
    def paginator(self, query_set):
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

class BaseAPIAnonymousView(CustomAPIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        # có bearer token trong header thì check token mới hoạt động
        if self.get_authorization_header(request).split():
            self.user = request.user
            

    @staticmethod
    def get_authorization_header(request):
        content = request.META.get('HTTP_AUTHORIZATION', b'')
        try:
            content = content.encode(HTTP_HEADER_ENCODING)
        except:
            content = b''
        return content

