# -*- coding: utf-8 -*-
# from odoo import http


# class OdooBasico(http.Controller):
#     @http.route('/odoo_basico_celia/odoo_basico_celia/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_basico_celia/odoo_basico_celia/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_basico_celia.listing', {
#             'root': '/odoo_basico_celia/odoo_basico_celia',
#             'objects': http.request.env['odoo_basico_celia.odoo_basico_celia'].search([]),
#         })

#     @http.route('/odoo_basico_celia/odoo_basico_celia/objects/<model("odoo_basico_celia.odoo_basico_celia"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_basico_celia.object', {
#             'object': obj
#         })
