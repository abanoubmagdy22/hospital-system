from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError
import re
from odoo.exceptions import ValidationError


class Patient(models.Model):
    _name = "hms.patient"
    _sql_constraints = [
        ('unique_email', 'unique (email)', 'Email address already exists!')
    ]

    # @api.depends("birthdate")
    # def calc_age(self):
    #     for patient in self:
    #         if patient.birthdate:
    #             d1 = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
    #
    #             d2 = date.today()
    #
    #             self.Age = relativedelta(d2, d1).years

    @api.depends('birthdate')
    def compute_age(self):
        for record in self:
            if record.birthdate and record.birthdate <= fields.Date.today():
                record.Age = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.birthdate)).years
            else:
                record.Age = 0

    firstname = fields.Char(required=True)
    lastname = fields.Char(required=True)
    birthdate = fields.Date()
    history = fields.Html()
    CR_Ratio = fields.Float()
    blood_type = fields.Selection([("A", 'a'), ("B", 'b'), ("O", 'o')])
    Pcr = fields.Boolean()
    image = fields.Binary()
    Address = fields.Text()
    Age = fields.Integer(compute="compute_age")
    department_id = fields.Many2one("hms.departments")
    department_name = fields.Char(related="department_id.name")
    patient_capacity = fields.Integer(related="department_id.capacity")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious'),
    ], default='good')
    description = fields.Text()
    email = fields.Text()

    tags_ids = fields.Many2many("hms.doctor.tag")

    @api.onchange('Age')
    def _onchange_Age(self):
        mess = ""
        if self.Age < 50:
            self.Pcr = True
            mess = "your age is less than 30"
        else:
            self.Pcr = False
            mess = "your age is more than 30"
        return {
            'warning': {
                'title': 'Hello',
                'message': mess
            },
        }

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match is None:
                raise ValidationError('Not a valid E-mail ID')

    # @api.onchange('Pcr')
    # def on_change_age(self):
    #     if self.Age < 30:
    #         raise UserError("your age is greater than 30")


class DoctorsTags(models.Model):
    _name = "hms.doctor.tag"
    name = fields.Char()
