# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrTaxStep(models.Model):
    _name = 'hr.tax.step'
    _inherit = ['mail.thread','mail.activity.mixin']

    tax_profile_id = fields.Many2one('hr.tax.profile', 'Tax Profile')
    low = fields.Float('Low Limit', help='Start of Tax Range')
    high = fields.Float("High Limit", help="End of Tax Range")
    rate = fields.Float('Rate', help='Tax Rate of This Range')


class HrTaxProfile(models.Model):
    _name = 'hr.tax.profile'
    _description = "Tax Profile is related to pay periods and payslips to specify tax type"
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char('Name')
    individual = fields.Boolean('Individual')
    step_ids = fields.One2many('hr.tax.step', 'tax_profile_id', 'Tax Steps')
