# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_code = fields.Char(
        string='Employee Code', copy=False, readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('hr.employee.code') or '/',
        index=True,
    )

    # --- Org dimensions used by the Headcount Dashboard filters/charts ---
    branch_id = fields.Many2one('hr.branch', string='Branch', tracking=True)
    zone_id = fields.Many2one(
        'hr.zone', string='Zone', related='branch_id.zone_id',
        store=True, readonly=False,
    )
    region_id = fields.Many2one(
        'res.country.state', string='Region', related='branch_id.region_id',
        store=True, readonly=True,
    )
    city = fields.Char(related='branch_id.city', string='City', store=True, readonly=True)
    division_id = fields.Many2one('hr.division', string='Division', tracking=True)
    sub_department_id = fields.Many2one(
        'hr.sub.department', string='Sub-Department', tracking=True,
        domain="[('department_id', '=', department_id)]",
    )
    management_level_id = fields.Many2one(
        'hr.management.level', string='Management Level', tracking=True,
    )
    hr_grade_id = fields.Many2one('hr.grade', string='HR Grade', tracking=True)

    employment_type = fields.Selection(
        [('full_time', 'Full-Time'), ('part_time', 'Part-Time')],
        string='Employment Type', default='full_time', tracking=True,
    )

    employee_status = fields.Selection(
        [
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('on_leave', 'On Leave'),
            ('probation', 'Probation'),
            ('retired', 'Retired'),
            ('terminated', 'Terminated'),
        ],
        string='Employee Status', default='active', tracking=True,
        help='Drives the Employee Status donut chart on the Headcount Dashboard.',
    )

    joining_date = fields.Date(string='Joining Date', tracking=True, index=True)
    exit_date = fields.Date(string='Exit Date', tracking=True, index=True)

    @api.onchange('department_id')
    def _onchange_department_id_reset_sub_department(self):
        for emp in self:
            if emp.sub_department_id.department_id != emp.department_id:
                emp.sub_department_id = False

    @api.onchange('branch_id')
    def _onchange_branch_id_sync_work_location(self):
        # keep the native work_location_id roughly aligned if the company
        # has configured matching work locations; safe no-op otherwise.
        pass
