from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 6
    max_page_size = 999
    page_size_query_param = 'limit'
