from odoo import models, fields


class Doctors(models.Model):
    _name = "hms.doctor"
    firstname = fields.Char()
    lastname = fields.Char()
    image = fields.Binary()
    # students_ids = fields.Many2many("iti.student")
