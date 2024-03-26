import pytest

from apps.products_catalogue.models import DeliveryMethod


@pytest.fixture
def fixture_delivery_method():
    return DeliveryMethod.objects.create(name='Standard', price=10.00)


@pytest.mark.django_db
def test_delivery_method_creation():
    assert 0 == DeliveryMethod.objects.count()
    method = DeliveryMethod.objects.create(name='Standard', price=10.00) 
    tested_method = DeliveryMethod.objects.get(id=method.id)
    assert tested_method.name == 'Standard'  
    assert tested_method.price == 10.00    


