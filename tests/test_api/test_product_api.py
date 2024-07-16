
import pytest
from datetime import datetime


url_of_get = '/api/netcaixa/stock/product'


def test_get_(client):
    """
    This method is  used to  test the get method 
    from product api
    """
    response = client.get(url_of_get)
   

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
    """
    This method is used to test the post method
    of the  product
    """
    dataForm = {  
                'barcode': "005",
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
    
    assert response.data == f'Response: False'.encode()
    
    # Line of code to test the success test
    #assert response.get_json() == [{"message":"Test passed", "category": "success", "object": 1},200]

    # Method to test the putch request method of the product


    


    