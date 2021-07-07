from typing import Optional

from django.db.models import QuerySet
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import View


class PaginationTotalPages(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

    def paginate_queryset(
        self,
        queryset: QuerySet,
        request: Request,
        view: Optional[View] = ...
    ) -> list:
        if not queryset.ordered:
            queryset = queryset.order_by('id')
        return (super(PaginationTotalPages, self)
                .paginate_queryset(queryset=queryset, request=request, view=view))

    def get_paginated_response(self, data):
        uri = self.request.build_absolute_uri().split('?')[0]
        pages = [x for x in range(1, self.page.paginator.num_pages + 1)]

        total_pages = len(pages)
        return Response({
            'next': self.get_next_link(),
            'base_link': uri + '?page=',
            'previous': self.get_previous_link(),
            'pages': pages,
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'start_index': self.page.start_index(),
            'end_index': self.page.end_index(),
            'page_size': self.page.paginator.per_page,
            'results': data,
            'total_pages': total_pages
        })
