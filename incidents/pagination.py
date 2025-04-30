from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

class ArticleLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 5
class ArticlePageNumberPagination(PageNumberPagination):
    page_size = 3

