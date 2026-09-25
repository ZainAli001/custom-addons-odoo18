# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import http
from odoo.http import request


def _to_date(value, default=None):
    if not value:
        return default
    return date.fromisoformat(value[:10])


def _pct_change(current, previous):
    if not previous:
        return 0.0 if not current else 100.0
    return round(((current - previous) / previous) * 100.0, 1)


class HeadcountDashboardController(http.Controller):

    # ---------------------------------------------------------------
    # Domain builder
    # ---------------------------------------------------------------
    def _build_domain(self, filters):
        domain = []
        mapping = {
            'region_id': 'region_id',
            'zone_id': 'zone_id',
            'branch_id': 'branch_id',
            'division_id': 'division_id',
            'department_id': 'department_id',
            'sub_department_id': 'sub_department_id',
            'job_id': 'job_id',
            'management_level_id': 'management_level_id',
            'hr_grade_id': 'hr_grade_id',
            'employment_type': 'employment_type',
            'employee_status': 'employee_status',
            'gender': 'gender',
        }
        for key, field_name in mapping.items():
            value = filters.get(key)
            if value:
                domain.append((field_name, '=', value))
        if filters.get('city'):
            domain.append(('city', 'ilike', filters['city']))
        return domain

    # ---------------------------------------------------------------
    # Main endpoint
    # ---------------------------------------------------------------
    @http.route('/hr_headcount_dashboard/data', type='json', auth='user')
    def get_dashboard_data(self, filters=None, offset=0, limit=10):
        filters = filters or {}
        Employee = request.env['hr.employee'].sudo()
        Job = request.env['hr.job'].sudo()

        date_to = _to_date(filters.get('date_to'), date.today())
        date_from = _to_date(filters.get('date_from'), date_to - relativedelta(months=1))
        period_len = (date_to - date_from).days + 1
        prev_date_to = date_from - relativedelta(days=1)
        prev_date_from = prev_date_to - relativedelta(days=period_len - 1)

        domain = self._build_domain(filters)
        # snapshot domain: employees that existed at/ before date_to and
        # (not yet exited, or exited after date_to)
        snapshot_domain = domain + [
            '|', ('exit_date', '=', False), ('exit_date', '>', date_to),
        ]

        employees = Employee.with_context(active_test=False).search(snapshot_domain)

        # --- KPI cards -------------------------------------------------
        total_employees = len(employees)
        active_employees = len(employees.filtered(lambda e: e.employee_status == 'active'))
        inactive_employees = len(employees.filtered(
            lambda e: e.employee_status in ('inactive', 'terminated')))
        on_probation = len(employees.filtered(lambda e: e.employee_status == 'probation'))

        new_joiners = Employee.with_context(active_test=False).search_count(
            domain + [('joining_date', '>=', date_from), ('joining_date', '<=', date_to)])
        ex_employees = Employee.with_context(active_test=False).search_count(
            domain + [('exit_date', '>=', date_from), ('exit_date', '<=', date_to)])

        # previous period, for the "vs last month" deltas
        prev_snapshot_domain = domain + [
            '|', ('exit_date', '=', False), ('exit_date', '>', prev_date_to),
            ('joining_date', '<=', prev_date_to),
        ]
        prev_total = Employee.with_context(active_test=False).search_count(prev_snapshot_domain)
        prev_active = Employee.with_context(active_test=False).search_count(
            prev_snapshot_domain + [('employee_status', '=', 'active')])
        prev_inactive = Employee.with_context(active_test=False).search_count(
            prev_snapshot_domain + [('employee_status', 'in', ('inactive', 'terminated'))])
        prev_new_joiners = Employee.with_context(active_test=False).search_count(
            domain + [('joining_date', '>=', prev_date_from), ('joining_date', '<=', prev_date_to)])
        prev_ex_employees = Employee.with_context(active_test=False).search_count(
            domain + [('exit_date', '>=', prev_date_from), ('exit_date', '<=', prev_date_to)])
        prev_on_probation = Employee.with_context(active_test=False).search_count(
            prev_snapshot_domain + [('employee_status', '=', 'probation')])

        # --- Positions (hr.job) ----------------------------------------
        job_domain = []
        if filters.get('department_id'):
            job_domain.append(('department_id', '=', filters['department_id']))
        if filters.get('branch_id'):
            job_domain.append(('branch_id', '=', filters['branch_id']))
        if filters.get('division_id'):
            job_domain.append(('division_id', '=', filters['division_id']))
        jobs = Job.search(job_domain)
        total_positions = int(sum(j.expected_employees or 0 for j in jobs))
        filled_positions = int(sum(j.no_of_employee or 0 for j in jobs))
        open_positions = int(sum(
            j.no_of_recruitment or 0 for j in jobs if j.state == 'recruit'))
        vacant_positions = max(total_positions - filled_positions - open_positions, 0)

        prev_open_positions = open_positions  # hr.job has no history; static baseline
        prev_vacant_positions = vacant_positions
        prev_total_positions = total_positions

        kpis = {
            'total_employees': {
                'value': total_employees,
                'delta': _pct_change(total_employees, prev_total)},
            'active_employees': {
                'value': active_employees,
                'delta': _pct_change(active_employees, prev_active)},
            'inactive_employees': {
                'value': inactive_employees,
                'delta': _pct_change(inactive_employees, prev_inactive)},
            'new_joiners': {
                'value': new_joiners,
                'delta': _pct_change(new_joiners, prev_new_joiners)},
            'ex_employees': {
                'value': ex_employees,
                'delta': _pct_change(ex_employees, prev_ex_employees)},
            'open_positions': {
                'value': open_positions,
                'delta': _pct_change(open_positions, prev_open_positions)},
            'vacant_positions': {
                'value': vacant_positions,
                'delta': _pct_change(vacant_positions, prev_vacant_positions)},
            'on_probation': {
                'value': on_probation,
                'delta': _pct_change(on_probation, prev_on_probation)},
        }

        # --- Charts ------------------------------------------------------
        charts = {
            'headcount_by_region_zone': self._chart_region_zone(employees),
            'headcount_by_department': self._chart_by_department(employees),
            'employee_status': self._chart_by_selection(employees, 'employee_status'),
            'gender_ratio': self._chart_by_selection(employees, 'gender'),
            'full_time_part_time': self._chart_by_selection(employees, 'employment_type'),
            'monthly_headcount_trend': self._chart_monthly_trend(Employee, domain, date_to),
            'new_joiners_vs_exits': self._chart_joiners_vs_exits(Employee, domain, date_to),
            'position_status': {
                'total': total_positions,
                'filled': filled_positions,
                'vacant': vacant_positions,
                'open': open_positions,
            },
        }

        # --- Employee list (paginated) -----------------------------------
        total_count = len(employees)
        page_records = employees.sorted('id')[offset:offset + limit]
        employee_list = [{
            'id': e.id,
            'employee_code': e.employee_code,
            'name': e.name,
            'region': e.region_id.name or '',
            'zone': e.zone_id.name or '',
            'branch': e.branch_id.name or '',
            'department': e.department_id.name or '',
            'designation': e.job_id.name or e.job_title or '',
            'management_level': e.management_level_id.name or '',
            'hr_grade': e.hr_grade_id.name or '',
            'employment_type': dict(e._fields['employment_type'].selection).get(
                e.employment_type, ''),
            'status': dict(e._fields['employee_status'].selection).get(
                e.employee_status, ''),
            'joining_date': e.joining_date.isoformat() if e.joining_date else '',
        } for e in page_records]

        return {
            'kpis': kpis,
            'charts': charts,
            'employees': employee_list,
            'employee_count': total_count,
        }

    # ---------------------------------------------------------------
    # Chart helpers
    # ---------------------------------------------------------------
    def _chart_region_zone(self, employees):
        by_region = defaultdict(int)
        by_region_zone = defaultdict(lambda: defaultdict(int))
        for e in employees:
            region_name = e.region_id.name or 'Unassigned'
            zone_name = e.zone_id.name or 'Unassigned'
            by_region[region_name] += 1
            by_region_zone[region_name][zone_name] += 1

        labels = sorted(by_region, key=lambda r: by_region[r], reverse=True)
        region_series = [by_region[r] for r in labels]
        zone_series = []
        for r in labels:
            zones = by_region_zone[r]
            zone_series.append(max(zones.values()) if zones else 0)
        return {'labels': labels, 'region': region_series, 'zone': zone_series}

    def _chart_by_department(self, employees):
        counts = defaultdict(int)
        for e in employees:
            counts[e.department_id.name or 'Unassigned'] += 1
        labels = sorted(counts, key=lambda d: counts[d], reverse=True)
        return {'labels': labels, 'values': [counts[l] for l in labels]}

    def _chart_by_selection(self, employees, field_name):
        selection = dict(employees._fields[field_name].selection)
        counts = defaultdict(int)
        for e in employees:
            key = getattr(e, field_name) or False
            label = selection.get(key, 'Unassigned') if key else 'Unassigned'
            counts[label] += 1
        total = sum(counts.values()) or 1
        return {
            'labels': list(counts.keys()),
            'values': list(counts.values()),
            'percentages': [round(v * 100.0 / total, 1) for v in counts.values()],
        }

    def _chart_monthly_trend(self, Employee, domain, date_to, months=6):
        labels, totals, actives = [], [], []
        for i in range(months - 1, -1, -1):
            month_end = (date_to.replace(day=1) - relativedelta(months=i)
                         + relativedelta(months=1) - relativedelta(days=1))
            month_domain = domain + [
                ('joining_date', '<=', month_end),
                '|', ('exit_date', '=', False), ('exit_date', '>', month_end),
            ]
            total = Employee.with_context(active_test=False).search_count(month_domain)
            active = Employee.with_context(active_test=False).search_count(
                month_domain + [('employee_status', '=', 'active')])
            labels.append(month_end.strftime('%b %Y'))
            totals.append(total)
            actives.append(active)
        return {'labels': labels, 'total_headcount': totals, 'active_headcount': actives}

    def _chart_joiners_vs_exits(self, Employee, domain, date_to, months=6):
        labels, joiners, exits = [], [], []
        for i in range(months - 1, -1, -1):
            month_start = (date_to.replace(day=1) - relativedelta(months=i))
            month_end = month_start + relativedelta(months=1) - relativedelta(days=1)
            j_count = Employee.with_context(active_test=False).search_count(
                domain + [('joining_date', '>=', month_start), ('joining_date', '<=', month_end)])
            e_count = Employee.with_context(active_test=False).search_count(
                domain + [('exit_date', '>=', month_start), ('exit_date', '<=', month_end)])
            labels.append(month_start.strftime('%b %Y'))
            joiners.append(j_count)
            exits.append(e_count)
        return {'labels': labels, 'new_joiners': joiners, 'exits': exits}

    # ---------------------------------------------------------------
    # Filter option lists (populate the dropdowns)
    # ---------------------------------------------------------------
    @http.route('/hr_headcount_dashboard/filter_options', type='json', auth='user')
    def get_filter_options(self):
        env = request.env
        def opts(records, label_field='name'):
            return [{'id': r.id, 'name': getattr(r, label_field)} for r in records]

        return {
            'regions': opts(env['res.country.state'].sudo().search([('id', 'in', env['hr.branch'].sudo().search([]).region_id.ids)])),
            'zones': opts(env['hr.zone'].sudo().search([])),
            'branches': opts(env['hr.branch'].sudo().search([])),
            'divisions': opts(env['hr.division'].sudo().search([])),
            'departments': opts(env['hr.department'].sudo().search([])),
            'sub_departments': opts(env['hr.sub.department'].sudo().search([])),
            'jobs': opts(env['hr.job'].sudo().search([])),
            'management_levels': opts(env['hr.management.level'].sudo().search([])),
            'hr_grades': opts(env['hr.grade'].sudo().search([])),
        }
