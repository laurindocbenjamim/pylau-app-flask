import pytest
from app import create_app
from flask import url_for
from datetime import datetime


url = '/netcaixa/stock'

def test_get(client):
    """
    This method is used to test the get method
    of the  product
    """
    response = client.get(f'{url}/select/all')
    # Line of code to test the staus
    assert response.status_code == 200

    #assert response.data == f'Response: True'.encode()
    
    # Line of code to test the success test
    assert response.get_json() == [{"status":True, "object": 2}, 200]

    # Method to test the putch request method of the product

@pytest.mark.parametrize("id",[(2)])
def test_get_by_id(client, id):
    """ This method is used to get the product by ID """
    response = client.get(f'{url}/select/{id}')
    # Line of code to test the staus
    assert response.status_code == 200

    assert response.get_json() == [{"status":True, "object": int(id)}, 200]
    #assert response.data == f'ID {id}'.encode()

@pytest.mark.parametrize("barcode", [("0299")])
def test_get_by_barcode(client, barcode):
    """ This method is used to get the product by barcode """
     
    response = client.post(f'{url}/select/by', data={'barcode': barcode})
    # Line of code to test the staus
    assert response.status_code == 200

    #assert response.get_json() == [{"status":True, "object": barcode }, 200]
    assert response.get_json() == [{"category": f"404 Not Found: No product with the barcode [{barcode}] has been found.", }, 400]
    #assert response.data == f'BARCODE: {barcode}'.encode()

params = [(1)]
@pytest.mark.parametrize("item",[('02994')])
def test_delete_by_id(client, item):
    """ This method is used to get the product by ID """
    response = client.get(f'{url}/delete/{item}/stock')
    # Line of code to test the staus
    assert response.status_code == 200

    #assert response.get_json() == [{"status": False, "category": "success"},200]
    assert response.data == f'The item {item} has been removed successfully.'.encode()
