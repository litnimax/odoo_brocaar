# -*- coding: utf-8 -*-
from odoo import http

# class Lorawan(http.Controller):
#     @http.route('/lorawan/lorawan/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lorawan/lorawan/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('lorawan.listing', {
#             'root': '/lorawan/lorawan',
#             'objects': http.request.env['lorawan.lorawan'].search([]),
#         })

#     @http.route('/lorawan/lorawan/objects/<model("lorawan.lorawan"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lorawan.object', {
#             'object': obj
#         })