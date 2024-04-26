""" from flask import Flask, jsonify


app = Flask("Test")

@app.route('/', methods=['GET'])
def index():
    return jsonify({"sms": "Ola mundo"})

@app.route('/person/<name>', methods=['GET'])
def person(name):
    return  f"My name is {name}"

if __name__ == '__main__':
    app.run(debug=True)

"""


import core
app = core.create_application()
app.run(debug=True)
