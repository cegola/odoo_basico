# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import Warning
import locale
import pytz


class informacion(models.Model):
    _name = 'odoo_basico_celia.informacion'  # será el nombre de la tabla (nombre modulo, nombre tabla)
    _description = 'Tipos de datos basicos'
    _order = "descripcion desc"
    _sql_constraints = [('nome unico', 'unique(name)', 'Non se pode repetir o nome')]

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

    data = fields.Date(string="Data", default=lambda self: fields.Date.today())
    data_hora = fields.Datetime(string="Data e Hora", default=lambda self: fields.Datetime.now())
    hora_utc = fields.Char(compute="_hora_utc", string="Hora UTC", size=15, store=True)
    hora_timezone_usuario = fields.Char(compute="_hora_timezone_usuario", string="Hora Timezone do Usuario", size=15,
                                        store=True)
    hora_actual = fields.Char(compute="_hora_actual", string="Hora Actual", size=15, store=True)

    mes_castelan = fields.Char(compute="_mes_castelan", size=15, string="Mes castelan", store="True")
    mes_galego = fields.Char(compute="_mes_galego", size=15, string="Mes galego", store="True")

    @api.constrains('peso')  # Ao usar ValidationError temos que importar a libreria ValidationError
    def _constrain_peso(self):  # from odoo.exceptions import ValidationError
        for rexistro in self:
            if rexistro.peso < 1 or rexistro.peso > 4:
                raise ValidationError('Os peso de %s ten que ser entre 1 e 4 ' % rexistro.name)


    @api.onchange('alto_cm')
    def _avisoAlto(self):
        for rexistro in self:  # Ao usar warning temos que importar a libreria from odoo.exceptions import Warning
            if rexistro.alto_cm > 7:
                raise Warning('O alto ten un valor posiblemente excesivo %s é maior que 7' % rexistro.alto_cm)


    @api.depends('alto_cm', 'largo_cm', 'ancho_cm')
    def _volumen(self):
        for registro in self:
            registro.volumen = float(registro.alto_cm) * float(registro.largo_cm) * float(registro.ancho_cm)

    @api.depends('peso', 'volumen')
    def _densidad(self):
        for registro in self:
            if registro.volumen != 0:
                registro.densidad = (float(registro.peso) / float(registro.volumen)) * 100
            else:
                registro.densidad = 0

    def _cambia_campo_sexo(self, rexistro):
        rexistro.sexo_traducido = "Hombre"

    def ver_contexto(self):  # Este método é chamado dende un botón de informacion.xml
        for rexistro in self:  # Ao usar warning temos que importar a libreria from odoo.exceptions import Warning
            raise Warning(
                'Contexto: %s' % rexistro.env.context)  # env.context é un diccionario  https://www.w3schools.com/python/python_dictionaries.asp
        return True

    @api.depends('data')
    def _mes_castelan(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')  # Para GNU/Linux
        # locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Para Windows
        for rexistro in self:
            rexistro.mes_castelan = rexistro.data.strftime("%B")  # strftime https://strftime.org/

    @api.depends('data')
    def _mes_galego(self):
        # O idioma por defecto é o configurado en locale na máquina onde se executa odoo.
        # Podemos cambialo con locale.setlocale, os idiomas teñen que estar instalados na máquina onde se executa odoo.
        # Lista onde podemos ver os distintos valores: https://docs.moodle.org/dev/Table_of_locales#Table
        locale.setlocale(locale.LC_TIME, 'gl_ES.utf8')  # Para GNU/Linux
        # locale.setlocale(locale.LC_TIME, 'Galician_Spain.1252')  # Para Windows
        for rexistro in self:
            rexistro.mes_galego = rexistro.data.strftime("%B")
        locale.setlocale(locale.LC_TIME, 'es_ES.utf8')  # Para GNU/Linux
        # locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Para Windows

    @api.depends('data_hora')
    def _hora_utc(self):
        for rexistro in self:  # A hora se almacena na BD en horario UTC (2 horas menos no verán, 1 hora menos no inverno)
            rexistro.hora_utc = rexistro.data_hora.strftime("%H:%M:%S")

    def actualiza_hora_actual_UTC(
            self):  # Esta función é chamada dende un boton de informacion.xml e dende _hora_actual
        for rexistro in self:
            rexistro.hora_actual = fields.Datetime.now().strftime("%H:%M:%S")
        # Grava a hora en UTC, se quixesemos poderiamos usar a función  _convirte_data_hora_de_utc_a_timezone_do_usuario

    @api.depends('data_hora')
    def _hora_actual(self):
        for rexistro in self:
            rexistro.actualiza_hora_actual_UTC()
        # Esta función será chamada dende a función actualiza_hora_timezone_usuario_dende_boton_e_apidepends e
        #  dende pedido.py (Cando insertamos os valores do template self.env.user.tz non ten o timezone do usuario por iso se carga coa hora UTC,
        #  o botón en pedido.py é para actualizar todos os rexistros masivamente dende outro modelo)

    def convirte_data_hora_de_utc_a_timezone_do_usuario(self,data_hora_utc_object):  # recibe a data hora en formato object
        usuario_timezone = pytz.timezone(self.env.user.tz or 'UTC')  # obter a zona horaria do usuario. Ollo!!! nas preferencias do usuario ten que estar ben configurada a zona horaria
        return pytz.UTC.localize(data_hora_utc_object).astimezone(usuario_timezone)  # hora co horario do usuario en formato object
        # para usar  pytz temos que facer  import pytz

    def actualiza_hora_timezone_usuario(self, obxeto_rexistro):
        obxeto_rexistro.hora_timezone_usuario = self.convirte_data_hora_de_utc_a_timezone_do_usuario(
            obxeto_rexistro.data_hora).strftime("%H:%M:%S")  # Convertimos a hora de UTC a hora do timezone do usuario

    def actualiza_hora_timezone_usuario_dende_boton_e_apidepends(
            self):  # Esta función é chamada dende un boton de informacion.xml e dende @api.depends _hora_timezone_usuario
        self.actualiza_hora_timezone_usuario(
            self)  # leva self como parametro por que actualiza_hora_timezone_usuario ten 2 parametros
        # porque usamos tamén actualiza_hora_timezone_usuario dende outro modelo (pedido.py) e lle pasamos como parámetro o obxeto_rexistro

    @api.depends('data_hora')
    def _hora_timezone_usuario(self):
        for rexistro in self:
            rexistro.actualiza_hora_timezone_usuario_dende_boton_e_apidepends()

    def envio_email(self):
        meu_usuario = self.env.user
        # mail_de     Odoo pon o email que configuramos en gmail para facer o envio
        mail_reply_to = meu_usuario.partner_id.email  # o enderezo email que ten asociado o noso usuario
        mail_para = 'cglclase@gmail.com'  # o enderezo email de destino
        mail_valores = {
            'subject': 'Aquí iría o asunto do email ',
            'author_id': meu_usuario.id,
            'email_from': mail_reply_to,
            'email_to': mail_para,
            'message_type': 'email',
            'body_html': 'Aquí iría o corpo do email cos datos por exemplo de "%s" ' % self.descripcion,
        }
        mail_id = self.env['mail.mail'].create(mail_valores)
        mail_id.sudo().send()
        return True