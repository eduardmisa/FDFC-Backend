from rest_framework import pagination
from collections import OrderedDict
from rest_framework.response import Response

from django.core.paginator import InvalidPage
from rest_framework.exceptions import NotFound
# from django.utils import six
from django.utils.translation import ugettext_lazy as _

class SimplePageNumberPagination(pagination.PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'page-size'
    max_page_size = 50

    invalid_page_message = _('Invalid page.')

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None 

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:

            if len(queryset) < page_size : 
              page_number = 1

            self.page = paginator.page(page_number)

        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)













    def get_paginated_response(self, data, additional_info=None):
        content = [
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('page', self.page.number),
            ('additional_info', additional_info)
        ]
        return Response(OrderedDict(content))

