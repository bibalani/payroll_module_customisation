# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrInsuranceProfile(models.Model):

    _inherit = ['mail.thread','mail.activity.mixin']
    _name = 'hr.insurance.profile'

    name = fields.Char('Name')
    max_insurable_gross = fields.Float("Maximum Insurable Gross")
    employee_rate = fields.Float("Employee Insurance Rate", default=0.07)
    employer_rate = fields.Float("Employer Insurance Rate", default=0.2)
    unemployment_rate = fields.Float("Unemployment Insurance Rate", default=0.03)
    low_limit = fields.Float("Low Limit", help="Minimum full absence day")
    max_limit = fields.Float("Max Limit", help="Maximum full absence dat")
