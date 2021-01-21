# -*- coding: utf-8 -*-

from odoo import models, fields, api


class informacion(models.Model):
    _name = 'odoo_basico.informacion'  # será el nombre de la tabla (nombre modulo, nombre tabla)
    _description = 'Tipos de datos basicos'

    name = fields.Char(string="Título", required=True, size=20)  # unico campo obligatorio que se tiene que llamar asi
    descripcion = fields.Char(string="La descripción")
    autorizado = fields.Boolean(string="¿Está autorizado?", default=True)
    sexo_traducido = fields.Selection([('Hombre', 'Home'), ('Mujer', 'Muller'), ('Otros', 'Outros')], string="Género")
    alto_cm = fields.Integer(string="Altura en cm")
    largo_cm = fields.Integer(string="Largo en cm")
    ancho_cm = fields.Integer(string="Ancho en cm")
    volumen = fields.Float(compute="_volumen", store=True)
    peso = fields.Float(string="Peso", default=2.7, digits=(6, 2))
    densidad = fields.Float(compute="_densidad", store=True)

    @api.depends('alto_cm', 'largo_cm', 'ancho_cm')
    def _volumen(self):
        for registro in self:
            registro.volumen = float(registro.alto_cm) * float(registro.largo_cm) * float(registro.ancho_cm)

    @api.depends('peso', 'volumen')
    def _densidad(self):
        for registro in self:
            if registro.volumen != 0:
                registro.densidad = (float(registro.peso)/ float(registro.volumen)) * 100
            else:
                registro.densidad = 0
