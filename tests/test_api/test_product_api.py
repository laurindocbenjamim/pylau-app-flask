
from app import create_app

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



def test_get(client):
    """
    This method is used to test the get method
    from the API with parameters
    """
    response = client.get(f'{url_of_get}/')
