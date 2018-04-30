# -*- coding: utf-8 -*-
from odoo import http

# class Appserver(http.Controller):
#     @http.route('/appserver/appserver/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/appserver/appserver/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('appserver.listing', {
#             'root': '/appserver/appserver',
#             'objects': http.request.env['appserver.appserver'].search([]),
#         })

#     @http.route('/appserver/appserver/objects/<model("appserver.appserver"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('appserver.object', {
#             'object': obj
#         })