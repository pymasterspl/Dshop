"""
+ there is PriceChangeHistory model with relation to product, with fields: price, created_at, disabled_at.
- creating product creates first PriceChangeHistory object with disabled_at == null
- every price change on product creates new PriceChangeHistory object with current date and time, previous PriceChangeHistory has disabled_at set to current date and time. 
- current price of the product is equal to the most recent entry in PriceChangeHistory for this model

"""

import pytest
from freezegun import freeze_time
from apps.products_catalogue.models import PriceChangeHistory, Product, Category


# use https://pypi.org/project/freezegun/ for time management in tests
# add __init__ method to product and store current price in local variable
# in save check if price changed
# if price changed 
#   - update last existing PriceCHangeHistory object with disabled_at = current time
#   - create new PriceCHangeHistory with new price


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


@pytest.fixture
def create_product_with_cat():
    with freeze_time("2023-07-01"):
        category = Category.objects.create(name='Test Category', is_active=True)
        return Product.objects.create(
            name="first one",
            category=category,
            price=11,
            short_description="short desc",
            full_description="full_description"
        )


def last_price_change_date(product):
    return PriceChangeHistory.objects.filter(product=product).order_by('created_at').last().created_at


@pytest.mark.django_db
def test_product_creation_creates_price_change_history(create_product_with_cat):   
    product = create_product_with_cat
    assert PriceChangeHistory.objects.count() == 1


@pytest.mark.django_db
def test_single_lowest_price_in_30_days(create_product_with_cat):
    product = create_product_with_cat
    assert product.lowest_price_in_30_days == product.price


@pytest.mark.django_db
def test_many_pricechangehistory_count(create_product_with_cat):
    product = create_product_with_cat
    #upper already saved once
    product.price = 2
    product.save()
    product.price = 3
    product.save()
    product.price = 4
    product.save()
    assert PriceChangeHistory.objects.count() == 4


@pytest.mark.django_db
def test_many_lowest_price_in_30_days_all_now(create_product_with_cat):
    product = create_product_with_cat
    product.price = 10
    product.save()
    product.price = 100
    product.save()
    product.price = 0.1
    product.save()
    assert product.lowest_price_in_30_days == 0.1


@pytest.mark.django_db
def test_many_lowest_price_in_30_days(create_product_with_cat):
    with freeze_time("2023-07-01"):
        #old
        product = create_product_with_cat
        print(f"{last_price_change_date(product)=}")
        product.price = 0.1
        product.save()
    with freeze_time("2023-07-27"):
        #old
        product.price = 0.5
        product.save()
        print(f"{last_price_change_date(product)=}")
    with freeze_time("2023-07-28"):
        #old
        product.price = 0.05
        product.save()
        print(f"{last_price_change_date(product)=}")
    with freeze_time("2023-11-02"):
        #active
        product.price = 0.25
        product.save()
        print(f"{last_price_change_date(product)=}")
    with freeze_time("2023-11-03"):
        #active
        product.price = 1
        product.save()

    print(f"{last_price_change_date(product)=}")

    with freeze_time("2023-11-04"):
        assert product.lowest_price_in_30_days == 0.25


@pytest.mark.django_db
def test_single_old_lowest_price_in_30_days(create_product_with_cat):
    with freeze_time("2023-07-01"):
        product = create_product_with_cat
        product.price = 0.1
        product.save()
    with freeze_time("2023-11-04"):
        assert product.lowest_price_in_30_days == 0.1
    