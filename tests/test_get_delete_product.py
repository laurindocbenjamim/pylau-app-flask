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
    assert response.get_json() == [{"message":"List of products", "category": "success", "object": 10},200]

    # Method to test the putch request method of the product

@pytest.mark.parametrize(('id'),(('8')))
def test_get_by_id(client, id):
    """ This method is used to get the product by ID """
    response = client.get(f'{url}/{id}')
    # Line of code to test the staus
    assert response.status_code == 200

    #assert response.get_json() == [{"message":"Product selected", "category": "success", "object": 1},200]
    assert response.data == f'ID: {id}'.encode()

@pytest.mark.parametrize(('id'),(('9')))
def test_delete_by_id(client, id):
    """ This method is used to get the product by ID """
    response = client.get(f'{url}/{id}/delete')
    # Line of code to test the staus
    assert response.status_code == 200

    assert response.get_json() == [{"status": False, "category": "success"},200]
    #assert response.data == f'ID: {id}'.encode()
