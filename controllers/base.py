from flask.views import MethodView
from flask import request, jsonify
from petals_mis.app import db


class CrudResource(MethodView):
    _model = None
    _private_attrs = []

    def get(self, **kwargs):
        if request.args:
            response_objs = db.session.query(self._model).filter_by(**request.args).all()
        else:
            response_objs = db.session.query(self._model).filter().all()
        response_dict = [
            {key: value for key, value in obj.as_dict().items() if key not in self._private_attrs}
            for obj in response_objs]
        return jsonify({"payload": response_dict})

    def post(self, **kwargs):
        obj = self._model(**request.json)
        status = 200
        try:
            obj.save()
            response_dict = {
                "payload": {key: value for key, value in obj.as_dict().items() if key not in self._private_attrs}}
        except Exception as e:
            response_dict = {"payload": {}, "message": str(e)}
            status = 400
        return jsonify(response_dict), status
