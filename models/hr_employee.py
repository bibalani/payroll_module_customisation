# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = ['hr.employee',]
    _description = 'Employee'

    slip_ids = fields.One2many('hr.payslip', 'employee_id', string='Payslips', readonly=True)
    payslip_count = fields.Integer(compute='_compute_payslip_count', string='Payslip Count', groups="bi_hr_payroll.group_hr_payroll_user")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('wf_partner', 'WF Partner'),
        ('onboard', 'Onboard'),
        ('wait', 'WF Checkout'),
        ('checkout', 'Checkout'),
        ('system', 'System')],
        string='Status', default='draft', readonly=True, track_visibility='onchange', copy=False)


    def _compute_payslip_count(self):
        for employee in self:
            employee.payslip_count = len(employee.slip_ids)

    def action_draft(self):
        return self.write({'state':'draft'})

    def action_wf_partner(self):
        return self.write({'state':'wf_partner'})

    def action_onboard(self):
        return self.write({'state':'onboard'})

    def action_wait_checkout(self):
        return self.write({'state':'wait'})

    def action_checkout(self):
        return self.write({'state':'checkout'})

    def action_system(self):
        return self.write({'state':'system'})

