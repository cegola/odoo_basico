# -*- coding: utf-8 -*-

from odoo import models, fields, api


class pedido(models.Model):
    _name = 'odoo_basico_celia.pedido'  # será el nombre de la tabla (nombre modulo, nombre tabla)
    _description = 'Cabecera pedido'

    name = fields.Char(string="Identificador", required=True, size=20)  # unico campo obligatorio que se tiene que llamar asi
    # Os campos One2many Non se almacenan na BD
    lineapedido_ids = fields.One2many("odoo_basico_celia.lineapedido", 'pedido_id')

    def actualizadorSexo(self):
        informacion_ids = self.env['odoo_basico_celia.informacion'].search([('autorizado', '=', False)])
        for rexistro in informacion_ids:
            self.env['odoo_basico_celia.informacion']._cambia_campo_sexo(rexistro)