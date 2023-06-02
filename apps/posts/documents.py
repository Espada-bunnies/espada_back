import copy
from django_elasticsearch_dsl import Index, Document, fields
from elasticsearch_dsl import analyzer, token_filter
from apps.posts.models import Post


PostIndex = Index('posts')
PostIndex.settings(
    number_of_shards=5,
    number_of_replicas=1
)


stopword_filter = token_filter(
    'stopword_filter',
    type='stop',
    stopwords_path='analysis/stopwords.txt'
)


espada_analyzer = analyzer(
    name_or_instance='espada_analyzer',
    tokenizer='uax_url_email',
    filter=[
        'lowercase',
        stopword_filter,
        'english_morphology',
        'russian_morphology'
    ]
)


@PostIndex.doc_type
class PostDocument(Document):
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'first_name': fields.TextField(
            copy_to='full_name'
        ),
        'last_name': fields.TextField(
            copy_to='full_name'
        ),
        'username': fields.KeywordField(),
    })
    body = fields.TextField(
        analyzer=espada_analyzer
    )

    class Django:
        model = Post
        fields = ('id',)

    