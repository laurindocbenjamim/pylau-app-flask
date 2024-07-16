
from flask.views import MethodView
from flask import jsonify, request


class GroupAPI(MethodView):
    init_every_request = False

    def __init__(self, model):
        self.model = model
        #self.validator = generate_validator(model, create=True)

    def get(self):
        items = self.model.query.all()
        return jsonify([item.to_json() for item in items])

    def post(self):
        errors = self.validator.validate(request.json)

        if errors:
            return jsonify(errors), 400

        #db.session.add(self.model.from_json(request.json))
        #db.session.commit()
        #return jsonify(item.to_json())

