import pytest
from datetime import datetime
from flask_wtf.csrf import generate_csrf


url = "/netcaixa/stock/update"

testdata = [("02994", 14.45)]

@pytest.mark.parametrize("product_barcode, product_iva", testdata)
def test_update_product_stock(client, product_barcode, product_iva):
    """
    This method is used to test the post method
    of the  product
    """

    """
    Approach - Changes
    The following notation not allow you to use a string of numbers or int values 
    compound by more then one digit, by default it split the value number
    @pytest.mark.parametrize(('barcode'), (('02994')))
    def test_update_product_stock(client, product_barcode, product_iva):

    Solution - New code
    testdata = [("02994", 14.45)]

    @pytest.mark.parametrize("product_barcode, product_iva", testdata)
    def test_update_product_stock(client, product_barcode, product_iva):
    
    """

    """
    Input test: [product_iva=14.45]
    Output: [product_iva=14.45]
    """
    # Generate CSRF token
    with client.session_transaction() as sess:
        csrf_token = generate_csrf()

    dataForm = {  
                'csrf_token': csrf_token,
        "product_barcode": "02994",
        "product_description": "Arroz",
        "product_unitary_price": 12.33,
        "product_iva": product_iva,
        "product_iva_code": "ASA",
        "product_profit": 12.0,
        "product_quantity": 12,
        "stock_pos": "",
        "stock_location": "",
        "stock_code": "",
        "stock_date_updated": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    }
    response = client.put(f'{url}/{product_barcode}/stock', data=dataForm)
    # Line of code to test the staus
    assert response.status_code == 200
    # Line of code to test the string lenght
    #assert response.get_json() == [{"message":"This field must have less or equal 100 characters", "category": "error", "object": []},400]
    # Line of code to test the characters
    #assert response.get_json() == [{"message":"Invalid Characters detected", "category": "error", "object": []},400]

    #assert response.data == f"ID is required. ID {id}".encode()

    #assert response.data == f"Response: This product already exist.".encode()
    #assert response.data == f"Response: False".encode()
    assert response.data == f"Response: True".encode()

