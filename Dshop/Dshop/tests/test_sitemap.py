import pytest
from django.urls import reverse
import xml.etree.ElementTree as ET


@pytest.mark.django_db
def test_is_xml(client):
    url = reverse("django.contrib.sitemaps.views.sitemap")
    response = client.get(url)
    assert response.status_code == 200
    xml = response.content

    root = ET.fromstring(xml.decode())
    assert ET.iselement(root)