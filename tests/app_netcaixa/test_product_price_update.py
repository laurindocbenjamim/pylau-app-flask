
import pytest
from datetime import datetime

"""
This module  is used to test the product price package
using the post request method .
"""

url = '/netcaixa/stock/price'


#======================== Method to update prices

dataForm = [(19, 10.5, 17.55, 23.65, 60.55556)]

@pytest.mark.parametrize("product_price_id, sale_price_01, sale_price_02, sale_price_03, pos_sale_price", dataForm)
# Test post method to save data to the database
def test_update_prices(client, product_price_id, sale_price_01, sale_price_02, sale_price_03, pos_sale_price):
    """
    Approach - Test the POST  request method to save the product 
    price.

    Input: []

    """

    data_form = {
        "product_barcode": '---',
        "product_description": "---",
        "sale_price_01": sale_price_01,
        "sale_price_02": sale_price_02,
        "sale_price_03": sale_price_03,
        "pos_sale_price": pos_sale_price, 
    }

    response = client.put(f'{url}/update/{product_price_id}', data=data_form)

    """
    Input[barcode='']
    Output[response='The product barcode is required']
    """
    #assert response.data == "The product barcode is required".encode()

    #assert response.data == "The price has been updated! True. Object: ".encode()

    assert response.data == "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.".encode()