import pytest
from app import create_app
from flask import url_for
from datetime import datetime


url = '/netcaixa/stock/product'

def test_get(client):
    """
    This method is used to test the get method
    of the  product
    """
    response = client.get(url)
    # Line of code to test the staus
    assert response.status_code == 200

    #assert response.data == f'Response: True'.encode()
    
    # Line of code to test the success test
    assert response.get_json() == [{"status":True, "object": 12}, 200]

    # Method to test the putch request method of the product

@pytest.mark.parametrize(('id'),(('8')))
def test_get_by_id(client, id):
    """ This method is used to get the product by ID """
    response = client.get(f'{url}/select/{id}')
    # Line of code to test the staus
    assert response.status_code == 200

    assert response.get_json() == [{"status":True, "object": int(id)}, 200]
    #assert response.data == f'ID {id}'.encode()


def test_get_by_barcode(client):
    """ This method is used to get the product by barcode """
    barcode = "02992"
    response = client.post(f'{url}/select', data={"barcode":barcode})
    # Line of code to test the staus
    assert response.status_code == 200

    assert response.get_json() == [{"status":True, "object": barcode }, 200]
    #assert response.data == f'BARCODE: {id}'.encode()

@pytest.mark.parametrize(('id'),(('7')))
def test_delete_by_id(client, id):
    """ This method is used to get the product by ID """
    response = client.get(f'{url}/{id}/delete')
    # Line of code to test the staus
    assert response.status_code == 200

    assert response.get_json() == [{"status": False, "category": "success"},200]
    #assert response.data == f'ID: {id}'.encode()
