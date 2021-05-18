from odoo import fields, models


class CrmHmsHospital(models.Model):
    _inherit = "res.partner"
    related_patient_id = fields.Text()
    salary = fields.Integer()
