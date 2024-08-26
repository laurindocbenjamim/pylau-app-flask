
import pytest
from datetime import datetime

"""
This module  is used to test the product price package
using the post request method .
"""

url = '/netcaixa/stock/price'

dataForm = [("099288", "Rice", 12.5, 19.55, 0, 0, 25.75)]

@pytest.mark.parametrize("product_barcode, product_description, unitary_price, sale_price_01, sale_price_02, sale_price_03, pos_sale_price", dataForm)
# Test post method to save data to the database
def test_post(client, product_barcode, product_description, unitary_price, sale_price_01, sale_price_02, sale_price_03, pos_sale_price):
    """
    Approach - Test the POST  request method to save the product 
    price.

    Input: []

    """

    data_form = {
        "product_barcode": product_barcode,
        "product_description": product_description,
        "sale_price_01": sale_price_01,
        "sale_price_02": sale_price_02,
        "sale_price_03": sale_price_03,
        "pos_sale_price": pos_sale_price, 
        "stock_date_added":  datetime.now().date(),
        "stock_year_added": datetime.now().strftime("%Y"),
        "stock_month_added": datetime.now().strftime("%m"),
        "stock_datetime_added": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        "stock_date_updated": "",
    }

    response = client.post(f'{url}/create', data=data_form)
    #assert response.data == "ready to save".encode()

    """
    Input[barcode='']
    Output[response='The product barcode is required']
    """
    #assert response.data == "The product barcode is required".encode()

    assert response.data == "The price has been created! True. Object: ".encode()

    #assert response.data == "Failed to create the price. False".encode()