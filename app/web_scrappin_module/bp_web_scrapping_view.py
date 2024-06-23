from flask import Blueprint, request, jsonify
from .modules.extract_contries_data import extract_countries

bp = Blueprint('ws', __name__, url_prefix='/ws')

@bp.route('/api/countries', methods=['GET'])
def get_countries():

    phonenumberULR = (
        "https://worldpopulationreview.com/country-rankings/phone-number-length-by-country"
    )
    with_length = "https://www.iban.com/dialing-codes"
    url = "https://countrycode.org/"

    web_font=with_length
    df = extract_countries(web_font)
    #serialized_data = df.to_json(orient='records', date_format='iso')
    data = []
    for i, row in df.iterrows():
        data.append(dict(row))
    
    return jsonify({"EXTRACTED_FROM": web_font, "ELEMENTS_or_SIZE": len(data),  "OBJECTS":  data })