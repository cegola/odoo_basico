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

    def creaRexistroInformacion(self):
        creado_id = self.env['odoo_basico_celia.informacion'].create({'name': 'Creado dende pedido'})
        creado_id.descripcion = "Creado dende o modelo pedido"
        creado_id.autorizado = False

    def actualizaRexistroInformacion(self):
        informacion_id = self.env['odoo_basico_celia.informacion'].search([('name', '=', 'Creado dende pedido')])
        if informacion_id:
            informacion_id.name = "Actualizado ..."
            informacion_id.descripcion = "Actualizado dende o modelo pedido"
            informacion_id.sexo_traducido = "Mujer"

    def actualizadorHoraTimezone(self):
        informacion_ids = self.env['odoo_basico_celia.informacion'].search([])
        for rexistro in informacion_ids:
            self.env['odoo_basico_celia.informacion'].actualiza_hora_timezone_usuario(rexistro)