# -*- coding: utf-8 -*-

from odoo import models, fields, api


class informacion(models.Model):
    _name = 'odoo_basico_celia.informacion'  # será el nombre de la tabla (nombre modulo, nombre tabla)
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
    foto = fields.Binary(string='Foto')
    adjunto_nombre = fields.Char(string='Nombre adjunto')
    adjunto = fields.Binary(string='Archivo adjunto')

    moeda_id = fields.Many2one('res.currency', domain="[('position','=','after')]")
    gasto = fields.Monetary("Gasto", 'moeda_id')

    moeda_euro_id = fields.Many2one('res.currency',
                                    default=lambda self: self.env['res.currency'].search([('name', '=', "EUR")],
                                                                                         limit=1))
    gasto_en_euros = fields.Monetary("Gasto", 'moeda_euro_id')
    moeda_en_texto = fields.Char(related="moeda_id.currency_unit_label", string="Moeda en formato texto", store=True)
    creador_da_moeda = fields.Char(related="moeda_id.create_uid.login", string="Usuario creador da moeda", store=True)


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

    def _cambia_campo_sexo(self, rexistro):
        rexistro.sexo_traducido = "Hombre"
