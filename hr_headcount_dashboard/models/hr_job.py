# -*- coding: utf-8 -*-
from odoo import fields, models


class HrJob(models.Model):
    _inherit = 'hr.job'

    branch_id = fields.Many2one('hr.branch', string='Branch')
    division_id = fields.Many2one('hr.division', string='Division')

    @property
    def vacant_count(self):
        """Sanctioned slots not currently filled (whether or not the job
        is actively being recruited for)."""
        return max((self.expected_employees or 0) - (self.no_of_employee or 0), 0)
