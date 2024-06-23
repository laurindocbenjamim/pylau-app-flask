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

    df = extract_countries(url)
    #serialized_data = df.to_json(orient='records', date_format='iso')
    data = []
    for i, row in df.iterrows():
        data.append(dict(row))
    
    return jsonify({"obj":  data })