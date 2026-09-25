from dateutil.relativedelta import relativedelta
from odoo import api, models, fields


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def get_dashboard_data(self):
        """
        Ye function ek hi call me saara data return karega
        taake JS me baar baar call na karna pare.
        """
        return {
            "won_lost": self._get_won_lost_data(),
            "by_stage": self._get_leads_by_stage(),
            "monthly_trend": self._get_monthly_trend(),
        }

    def _get_won_lost_data(self):
        won = self.search_count([("stage_id.is_won", "=", True)])
        lost = self.with_context(active_test=False).search_count([("active", "=", False)])
        return {
            "labels": ["Won", "Lost"],
            "datasets": [{
                "data": [won, lost],
                "backgroundColor": ["#28a745", "#dc3545"],
                "hoverOffset": 4
            }]
        }

    def _get_leads_by_stage(self):
        # Group by Stage
        groups = self.read_group([], ['stage_id'], ['stage_id'])
        labels = []
        data = []

        for group in groups:
            # Stage ka naam uthayenge, agar nahi hai to 'Undefined'
            stage_name = group.get('stage_id') and group['stage_id'][1] or 'Undefined'
            labels.append(stage_name)
            data.append(group['stage_id_count'])

        return {
            "labels": labels,
            "datasets": [{
                "label": "Leads by Stage",
                "data": data,
                "backgroundColor": "#17a2b8",
            }]
        }

    def _get_monthly_trend(self):

        labels = []
        data = []
        today = fields.Date.context_today(self)


        for i in range(4, -1, -1):

            date_cursor = today - relativedelta(months=i)

            month_label = date_cursor.strftime('%B %Y')


            start_date = date_cursor.replace(day=1)
            end_date = start_date + relativedelta(months=1, days=-1)

            count = self.search_count([
                ('create_date', '>=', start_date),
                ('create_date', '<=', end_date)
            ])

            labels.append(month_label)
            data.append(count)

        return {
            "labels": labels,
            "datasets": [{
                "label": "New Leads Trend",
                "data": data,
                "borderColor": "#ffc107",
                "backgroundColor": "rgba(255, 193, 7, 0.2)",
                "fill": True,
                "tension": 0.4
            }]
        }

    # def _get_monthly_trend(self):
    #     # Group by Creation Date (Month)
    #     # Last 6 months ka data uthate hain
    #     domain = []
    #     groups = self.read_group(domain, ['create_date'], ['create_date:month'])
    #
    #     labels = []
    #     data = []
    #
    #     for group in groups:
    #         labels.append(group['create_date:month'])
    #         data.append(group['create_date_count'])
    #
    #     return {
    #         "labels": labels,
    #         "datasets": [{
    #             "label": "New Leads per Month",
    #             "data": data,
    #             "borderColor": "#ffc107",  # Yellow line
    #             "fill": False,
    #             "tension": 0.1  # Line curve
    #         }]
    #     }
