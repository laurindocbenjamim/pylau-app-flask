
import pytest
from datetime import datetime

url = '/reports/pdf/gen-prod-pdf'

def test_generate_product_report(client):

    assert client.get(url).status_code == 200
