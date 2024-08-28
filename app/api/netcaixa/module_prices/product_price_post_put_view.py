from datetime import datetime
from flask.views import View
from flask import request, jsonify, render_template, redirect
from .controller import validate_words


class ProductPricePostPutViev(View):
    """
    This class  is used to create the price View
    """

    methods = ["POST", "PUT"]

    def __init__(self, price, template) -> None:
        super().__init__()
        self._price = price
        self._template = template

    def dispatch_request(self, product_price_id: int = None):
        message = ""
        error = ""
        category = ""
        status = False

        # Function to validate our form data
        def validate_form():
            for key, value in request.form.items():
                status, sms = validate_words(key=key, value=value)
                if not status:
                    message = f"{sms}"
                    category = "error"
                    break
            return status
        
        # Function to update only the product informations
        def update_prod_info(price_id):
            status, obj = self._price.update_prices(price_id=price_id,price=
                    {
                        "product_barcode": request.form.get("product_barcode"),
                        "product_description": request.form.get("product_description"),
                        "stock_date_updated": "",
                    }
                )
            if status:
                return f"The product information has been updated! {status}. Object: "
            else:
                return f"Failed to update the product information. {status}"

        # Function to update the product prices
        def update_prices(product_barcode):
            status, obj = self._price.update_prices(product_price_id=product_price_id,price=
                    {
                        "sale_price_01": request.form.get("sale_price_01"),
                        "sale_price_02": request.form.get("sale_price_02"),
                        "sale_price_03": request.form.get("sale_price_03"),
                        "pos_sale_price": request.form.get("pos_sale_price"),
                        "stock_date_updated": "",
                    }
                )
            if status:
                return f"The price has been updated! {status}. Object: "
            else:
                return f"{obj}"

        

        if request.method == "POST":

            if validate_form():
                status, obj = self._price.create(
                    {
                        "product_barcode": request.form.get("product_barcode"),
                        "product_description": request.form.get("product_description"),
                        "sale_price_01": request.form.get("sale_price_01"),
                        "sale_price_02": request.form.get("sale_price_02"),
                        "sale_price_03": request.form.get("sale_price_03"),
                        "pos_sale_price": request.form.get("pos_sale_price"),
                        "stock_date_added": request.form.get("stock_date_added"),
                        "stock_year_added": request.form.get("stock_year_added"),
                        "stock_month_added": request.form.get("stock_month_added"),
                        "stock_datetime_added": request.form.get("stock_datetime_added"),
                        "stock_date_updated": "",
                    }
                )
                if status:
                    return f"The price has been created! {status}. Object: "
                else:
                    return f"Failed to create the price. {status}-"
            return f"Invalid form data"

            """ 
                Update the product prices.
                First check the form data is valid, if true it calls the method 
                update_prices otherwise return the validation responses or
                  the message 'Invalid form data'
            """
        elif request.method == "PUT":
            if product_price_id is None:
                return "Price ID required."
            else:
                if validate_form():
                    return update_prices(product_price_id)
            return f"Invalid form data"
        else:
            return f"Method not allowed!"
