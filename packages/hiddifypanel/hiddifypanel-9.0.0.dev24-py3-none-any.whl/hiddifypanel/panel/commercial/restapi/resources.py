from flask import abort, jsonify, request
from flask_restful import Resource
# from flask_simplelogin import login_required
import datetime
from hiddifypanel.models import *
from urllib.parse import urlparse
from hiddifypanel.panel import hiddify
from hiddifypanel.drivers import user_driver
# class AllResource(Resource):
#     def get(self):
#         return jsonify(
#             hiddify.dump_db_to_dict()
#         )


class UserResource(Resource):
    decorators = [hiddify.super_admin]

    def get(self, uuid=None):
        uuid = request.args['uuid'] if 'uuid' in request.args else None
        if uuid:
            product = User.query.filter(User.uuid == uuid).first() or abort(204)
            return jsonify(product.to_dict())

        products = User.query.all() or abort(204)
        return jsonify(
            [product.to_dict() for product in products]
        )

    def post(self):
        data = request.json
        # because add_client method accepts a user object not uuid the api returns 502 error.I have a possible fix for this
        user = User.query.filter(User.uuid == data['uuid']).first() or abort(204)
        hiddify.add_or_update_user(**data)
        user_driver.add_client(user)
        hiddify.quick_apply_users()

        return jsonify({'status': 200, 'msg': 'ok'})

        # start aliz dev
    # desc : it is better to have a delete method to manage users more programatically :)
    def delete(self, uuid=None):
        uuid = request.args['uuid'] if 'uuid' in request.args else None
        if uuid:
            user = User.query.filter(User.uuid == uuid).first() or abort(204)
            if user is not None:
                hiddify.remove_user(uuid)
                user_driver.remove_client(uuid)
                hiddify.quick_apply_users()
                return jsonify({'status': 200, 'msg': 'ok'})
            else:
                return jsonify({'status': 204, 'msg': 'user not found'})
        else:
            return jsonify({'status': 204, 'msg': 'uuid not found'})
    # end aliz dev


class AdminUserResource(Resource):
    decorators = [hiddify.super_admin]

    def get(self, uuid=None):
        uuid = request.args['uuid'] if 'uuid' in request.args else None
        if uuid:
            product = AdminUser.query.filter(AdminUser.uuid == uuid).first() or abort(204)
            return jsonify(product.to_dict())

        products = AdminUser.query.all() or abort(204)
        return jsonify(
            [product.to_dict() for product in products]
        )

    def post(self):
        data = request.json
        hiddify.add_or_update_admin(**data)

        return jsonify({'status': 200, 'msg': 'ok'})


# class DomainResource(Resource):
#     def get(self,domain=None):
#         if domain:
#             product = Domain.query.filter(Domain.domain==domain).first() or abort(204)
#             return jsonify(hiddify.domain_dict(product))
#         products = Domain.query.all() or abort(204)
#         return jsonify(
#             [hiddify.domain_dict(product) for product in products]
#         )
#     def post(self):
#         hiddify.add_or_update_domain(**request.json)
#         return jsonify({'status':200,'msg':'ok'})

# class ParentDomainResource(Resource):
#     def get(self,parent_domain=None):
#         if domain:
#             product = ParentDomain.query.filter(ParentDomain.domain==domain).first() or abort(204)
#             return jsonify(hiddify.parent_domain_dict(product))
#         products = ParentDomain.query.all() or abort(204)
#         return jsonify(
#             [hiddify.parent_domain_dict(product) for product in products]
#         )
#     def post(self):
#         hiddify.add_or_update_parent_domain(**request.json)
#         return jsonify({'status':200,'msg':'ok'})

# class ConfigResource(Resource):
#     def get(self,key=None,child_id=0):
#         if key:
#             return jsonify(hconfig(key,child_id))
#         return jsonify(get_hconfigs(child_id))

#     def post(self):
#         hiddify.add_or_update_config(**request.json)
#         return jsonify({'status':200,'msg':'ok'})

class HelloResource(Resource):
    def get(self):
        return jsonify({"status": 200, "msg": "ok"})


# class UpdateUsageResource(Resource):
#     def get(self):
#         return jsonify({"status": 200, "msg": "ok"})
