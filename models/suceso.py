
from odoo import models, fields, api


class suceso(models.Model):
    _name = 'odoo_basico_celia.suceso'  # será el nombre de la tabla (nombre modulo, nombre tabla)
    _description = 'Prueba vista tree en modo edición'

    name = fields.Char(string="Suceso", required=True, size=20)  # unico campo obligatorio que se tiene que llamar asi
    descripcion = fields.Char(string="La descripción del suceso")
    nivel = fields.Selection([('Alto', 'Alto'), ('Medio', 'Medio'), ('Bajo', 'Bajo')], string="Nivel")
    data_hora = fields.Datetime(string="Fecha y hora")