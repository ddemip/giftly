from haystack import indexes
from .models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='giftlyapp/product_text.txt')
    name = indexes.CharField(model_attr='name')
    categories = indexes.MultiValueField()

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

    def prepare_categories(self, obj):
        return [category.name for category in obj.categories.all()]
