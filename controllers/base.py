from flask.views import MethodView
from flask import request, jsonify
from flask import abort
from flask_jwt import current_identity

from petals_mis.app import db


class CrudResource(MethodView):
    _model = None
    _private_attrs = []
    _restrict_updates = []
    _allowed_methods = ["GET", "POST", "DELETE", "PUT"]

    def get(self, **kwargs):
        if "GET" not in self._allowed_methods:
            return abort(404)
        if request.args:
            response_objs = db.session.query(self._model).filter_by(**request.args).all()
        else:
            response_objs = db.session.query(self._model).filter().all()
        get_priority = getattr(self, "priority").get("GET")
        if get_priority and current_identity.priority < get_priority:
            return jsonify({"payload": {}, "message": "Restricted access"})
        response_dict = [
            {key: value for key, value in obj.as_dict().items() if key not in self._private_attrs}
            for obj in response_objs]
        return jsonify({"payload": response_dict})

    def post(self, **kwargs):
        if "POST" not in self._allowed_methods:
            return abort(404)
        get_priority = getattr(self, "priority").get("POST")
        if get_priority and current_identity.priority < get_priority:
            return jsonify({"payload": {}, "message": "Restricted access"})
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

    def delete(self, **kwargs):
        if "DELETE" not in self._allowed_methods:
            return abort(404)
        if not request.json.get("id"):
            return jsonify({"payload": {}, "message": "id has to be passed as a param"}), 400
        get_priority = getattr(self, "priority").get("DELETE")
        if get_priority and current_identity.priority < get_priority:
            return jsonify({"payload": {}, "message": "Restricted access"})
        try:
            model_obj = db.session.query(self._model).filter(self._model.id == request.json["id"]).first()
            model_obj.destroy()
            return jsonify({"payload": {}, "message": "Successfully Deleted"})
        except Exception as e:
            return jsonify({"payload": {}, "message": str(e)}), 400

    def put(self, **kwargs):
        if "PUT" not in self._allowed_methods:
            return abort(404)
        if not request.json.get("id"):
            return jsonify({"payload": {}, "message": "id has to be passed as a param"}), 400
        get_priority = getattr(self, "priority").get("PUT")
        if get_priority and current_identity.priority < get_priority:
            return jsonify({"payload": {}, "message": "Restricted access"})
        restricted_updates_on = ["created_at", "updated_at", "id"] + self._restrict_updates
        updatable_attrs = [
            key for key in self._model.__table__.columns.keys() if key not in restricted_updates_on]
        update_dict = {
            key: value for key, value in request.json.items() if key in updatable_attrs
        }
        model_obj = db.session.query(self._model).filter(self._model.id == request.json.get("id")).first()
        for key in update_dict:
            setattr(model_obj, key, update_dict[key])
        try:
            db.session.add(model_obj)
            db.session.commit()
            return jsonify({"payload": model_obj.as_dict()})
        except Exception as e:
            db.session.rollback()
            return jsonify({"payload": {}, "message": str(e)}), 400
