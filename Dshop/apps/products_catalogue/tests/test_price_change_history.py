"""
+ there is PriceChangeHistory model with relation to product, with fields: price, created_at, disabled_at.
- creating product creates first PriceChangeHistory object with disabled_at == null
- every price change on product creates new PriceChangeHistory object with current date and time, previous PriceChangeHistory has disabled_at set to current date and time. 
- current price of the product is equal to the most recent entry in PriceChangeHistory for this model

"""

import pytest
from apps.products_catalogue.models import PriceChangeHistory, Product, Category

@pytest.mark.django_db # to be deleted
def test_model_structure():
    # This kind of test is for fun mostly and will be deleted in going further. 
    # However, those simple tests have great unlocking power and allow to learn new stuff. 
    # There is nothing wrong in deleting obsolete test at some point:
    # Flow:
    # red
    # green
    # refactor

    # Given
    fields_to_check = ["product", "price", "created_at", "disabled_at"]
    # When
    model = PriceChangeHistory
    # Then
    for field in fields_to_check:
        assert model._meta.get_field(field)


@pytest.mark.django_db
def test_product_creation_creates_price_change_history():   
    # Given
    assert PriceChangeHistory.objects.count() == 0
    category = Category.objects.create(name='Test Category', is_active=True)

    # When
    product = Product.objects.create(
        name="first one",
        category=category,
        price=11,
        short_description="short desc",
        full_description="full_description"
    )
    # Then
    assert PriceChangeHistory.objects.count() == 1
