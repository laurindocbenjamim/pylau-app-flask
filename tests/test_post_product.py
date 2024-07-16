import pytest
from app import create_app
from flask import url_for
from datetime import datetime


url = '/netcaixa/stock/product'

def test_post(client):
    """
    This method is used to test the post method
    of the  product
    """
    dataForm = {  
                'barcode': "006",
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
    response = client.post(url, data=dataForm)
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

@pytest.mark.parametrize(('barcode', 'description', 'category', 'type','detail', 'brand'),
                         (
                             ('02994', 'Arrox', 'ss', 'ss','000', 'Food'),
                             ('02993', 'ss', 'ss', '','000', 'Food'),
                             ('ss3', 'Arrox', '', '','000', 'Food'),
                         ))
def test_validate_input_form(client, barcode, description, category, type, detail, brand):
    """
    This method is used to test the post method
    of the  product
    """
    dataForm = {  
                'barcode': barcode,
                'description': description,
                'category': category,
                'type': type ,   
                'detail': detail,
                'brand': brand,
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
    response = client.post(url, data=dataForm)
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
