import pytest
from app import create_app
from flask import url_for
from datetime import datetime


url = "/netcaixa/stock/create/stock"


def test_post(client):
    """
    This method is used to test the post method
    of the  product
    """
    dataForm = {
        "product_barcode": "02994",
        "product_description": "Arroz",
        "product_unitary_price": 12.3,
        "product_iva": 12.5,
        "product_iva_code": "ASA",
        "product_profit": 12.0,
        "product_quantity": 12,
        "stock_pos": "",
        "stock_location": "",
        "stock_code": "",
        "stock_date_added":  datetime.now().date(),
        "stock_year_added": datetime.now().strftime("%Y"),
        "stock_month_added": datetime.now().strftime("%m"),
        "stock_datetime_added": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        "stock_date_updated": "",
    }
    response = client.post(url, data=dataForm)
    # Line of code to test the staus
    assert response.status_code == 200
    # Line of code to test the string lenght
    # assert response.get_json() == [{"message":"This field must have less or equal 100 characters", "category": "error", "object": []},400]
    # Line of code to test the characters
    # assert response.get_json() == [{"message":"Invalid Characters detected", "category": "error", "object": []},400]

    # assert response.data == f"This field must be a string [brand]".encode()
    
    assert response.data == f"Response: True".encode()
    #assert response.data == f"Response: False".encode()

    # Line of code to test the success test
    # assert response.get_json() == [{"message":"Test passed", "category": "success", "object": 1},200]

    # Method to test the putch request method of the product


@pytest.mark.parametrize(
    ("barcode", "description", "unitary_price", "iva", "iva_code", "profit", "quantity"),
    (
        ("02994", "", "ss", "ss", "000", "Food", ''),
        ("02993", "ss", "", "", "000", "Food", 0),
        ("", "Arrox", "", "", "000", "Food", 0),
    ),
)
def test_validate_input_form(
    client, barcode, description, unitary_price, iva, iva_code, profit, quantity
):
    """
    This method is used to test the post method
    of the  product
    """
    dataForm = {
        "product_barcode": barcode,
        "product_description": description,
        "product_unitary_price": unitary_price,
        "product_iva": iva,
        "product_iva_code": iva_code,
        "product_profit": profit,
        "product_quantity": quantity,
        "stock_pos": "",
        "stock_location": "",
        "stock_code": "",
        "stock_date_added":  datetime.now().date(),
        "stock_year_added": datetime.now().strftime("%Y"),
        "stock_month_added": datetime.now().strftime("%m"),
        "stock_datetime_added": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        "stock_date_updated": "",
    }
    response = client.post(url, data=dataForm)
    # Line of code to test the staus
    assert response.status_code == 200
    # Line of code to test the string lenght
    # assert response.get_json() == [{"message":"This field must have less or equal 100 characters", "category": "error", "object": []},400]
    # Line of code to test the characters
    # assert response.get_json() == [{"message":"Invalid Characters detected", "category": "error", "object": []},400]

    # assert response.data == f"This field must be a string [brand]".encode()

    print(f"Response: {response.data}")
    assert response.data == f"Response: False".encode()

    # Line of code to test the success test
    # assert response.get_json() == [{"message":"Test passed", "category": "success", "object": 1},200]

    # Method to test the putch request method of the product
