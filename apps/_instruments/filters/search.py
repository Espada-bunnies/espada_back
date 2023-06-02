

from unicodedata import category
from elasticsearch_dsl import Q
from apps.posts.documents import PostDocument
from apps.posts.container import post_service


class SearchPosts:

    def filter_queryset(self, request, queryset, view):
        category = view.kwargs.get('category')
        query_text = request.query_params.get('search')
        if not query_text:
            return post_service.get_update_queryset(queryset, category)
        query = Q(
            'multi_match',
            query=query_text,
            fields=[
                'body',
                'user.full_name',
                'user.username'
            ],
            fuzziness=1,
            minimum_should_match=2,
        )
        search = PostDocument.search().query(query)
        return post_service.get_update_queryset(search.to_queryset(), category)