from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class CustomPagePagination(PageNumberPagination):
    """user defined pagination"""
    page_size = 6
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = 20

    def get_paginated_response(self, data):
        new_data = OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
        ])
        if 'code' in data:
            new_data['code'] = data.pop('code')
        if 'msg' in data:
            new_data['msg'] = data.pop('msg')
        if 'results' in data:
            new_data['results'] = data.pop('result')
        return Response(new_data)
