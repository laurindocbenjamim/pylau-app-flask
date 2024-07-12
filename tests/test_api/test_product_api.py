
import pytest
from app import create_app
from flask import url_for
from datetime import datetime


url_of_get = '/api/netcaixa/stock/product'

def test_config():
    """
    First test the application configuration
    """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_get_(client):
    """
    This method is  used to  test the get method 
    from product api
    """
    response = client.get(url_of_get)
    assert response.get_json() == [
            {
                'product_id': 1,  
                'product_barcode': "001",
                'product_description': "product1",
                'product_category': "Vegetal",
                'product_type': "Delicados" ,   
                'product_detail':"product do campo",
                'product_brand': "",
                'product_measure_unit': "unit",
                'product_fixed_margin': "10",
                'product_status': True,
                'product_retention_font': "",
                'product_date_added': "2024/09/09",
                'product_year_added': "2024",
                'product_month_added': "09",
                'product_datetime_added': "2024/09/09 23:03",
                'product_date_updated': "",
            },
            {
                'product_id': 2,  
                'product_barcode': "002",
                'product_description': "product2",
                'product_category': "Vegetal",
                'product_type': "Delicados" ,   
                'product_detail':"product do campo",
                'product_brand': "",
                'product_measure_unit': "unit",
                'product_fixed_margin': "10",
                'product_status': True,
                'product_retention_font': "",
                'product_date_added': "2024/09/09",
                'product_year_added': "2024",
                'product_month_added': "09",
                'product_datetime_added': "2024/09/09 23:03",
                'product_date_updated': "",
            },
        ]



def test_get_with_param(client):
    """
    This method is used to test the get method
    from the API with parameters
    """
    id = 11
    """
        Approach
        This cide does not work. It returns the error 'RuntimeError: Working outside of application context.'
    response = client.get(url_for('api/netcaixa/stock/product/', id=id))

        Change to:
    response = client.get(f'api/netcaixa/stock/product/{id}')

    """
    response = client.get(f'api/netcaixa/stock/product/{id}')
    assert response.status_code == 200
    assert response.get_json() == {"GET":f'Your ID {id}'}


class ProductAction(object):
    url_of_get = '/api/netcaixa/stock/product'

    def __init__(self, client) -> None:
        self._client = client

    def post(self):
        dataForm = {"barcode": "002992", "description": "arroz"}
        return self._client.post(self.url_of_get, data=dataForm)
    
@pytest.fixture
def product(client):
    return ProductAction(client)

def test_post(client):
    dataForm = {  
                'barcode': "003",
                'description': "Arroz Agulha",
                'category': "Vegetal",
                'type': "Delicados" ,   
                'detail':"product do campo",
                'brand': "",
                'measure_unit': "unit",
                'fixed_margin': "10",
                'status': True,
                'retention_font': "",
                'date_added': datetime.now().date(),
                'year_added': datetime.now().strftime('%Y'),
                'month_added': datetime.now().strftime('%m'),
                'datetime_added': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
                'date_updated': "",
            }
    response = client.post(url_of_get, data=dataForm)
    # Line of code to test the staus
    assert response.status_code == 200
    # Line of code to test the string lenght
    #assert response.get_json() == [{"message":"This field must have less or equal 100 characters", "category": "error", "object": []},400]
    # Line of code to test the characters
    #assert response.get_json() == [{"message":"Invalid Characters detected", "category": "error", "object": []},400]

    #assert response.data == f"This field must be a string [brand]".encode()
    
    assert response.data == f'Response: True'.encode()
    
    # Line of code to test the success test
    #assert response.get_json() == [{"message":"Test passed", "category": "success", "object": 1},200]
    