# -*- coding: utf-8 -*-
from odoo import http

# class Netserver(http.Controller):
#     @http.route('/netserver/netserver/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/netserver/netserver/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('netserver.listing', {
#             'root': '/netserver/netserver',
#             'objects': http.request.env['netserver.netserver'].search([]),
#         })

#     @http.route('/netserver/netserver/objects/<model("netserver.netserver"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('netserver.object', {
#             'object': obj
#         })