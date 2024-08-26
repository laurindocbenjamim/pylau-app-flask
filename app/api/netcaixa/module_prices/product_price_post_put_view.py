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

    def dispatch_request(self):

        message = ""
        error = ""
        category = ""
        status = False

        if request.method == "POST":
            for key, value in request.form.items():
                status, sms = validate_words(key=key, value=value)
                if not status:
                    message = f"{sms}"
                    category = "error"
                    break

            if status:
                status, obj = self._price.create(
                    {
                        "product_barcode": request.form.get("product_barcode"),
                        "product_description": request.form.get("product_description"),
                        "sale_price_01": request.form.get("sale_price_01"),
                        "sale_price_02": request.form.get("sale_price_02"),
                        "sale_price_03": request.form.get("sale_price_03"),
                        "pos_sale_price": request.form.get("pos_sale_price"),
                        "stock_date_added": datetime.now().date(),
                        "stock_year_added": datetime.now().strftime("%Y"),
                        "stock_month_added": datetime.now().strftime("%m"),
                        "stock_datetime_added": datetime.now().strftime(
                            "%Y/%m/%d %H:%M:%S"
                        ),
                        "stock_date_updated": "",
                    }
                )
                if status:
                    return f"The price has been created! {status}. Object: "
                else:
                    return f"Failed to create the price. {status}"
            return f"{message}"
        elif request.method == "PUT":
            return f"ready to update"
        else:
            return f"Method not allowed!"
