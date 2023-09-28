# Copyright 2023 Akretion (https://www.akretion.com).
# @author Matthieu SAISON <matthieu.saison@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    probability = fields.Integer(
        "Winning sale %",
        default=lambda self: self.env.ref(
            "sale_probability_amount.quotation_default_probability",
            raise_if_not_found=False,
        ).value,
    )

    expected_amount_cur = fields.Monetary(
        "Expected Amount in currency",
        compute="_compute_expected_amount_cur",
        currency_field="company_currency_id",
        store=True,
    )

    def action_confirm(self):
        self.probability = 100
        return super().action_confirm()

    def action_cancel(self):
        self.probability = 0
        return super().action_confirm()

    def action_draft(self):
        self.probability = 50
        return super().action_confirm()

    @api.depends("amount_total_curr", "probability")
    def _compute_expected_amount_cur(self):
        for record in self:
            record.expected_amount_cur = (
                record.amount_total_curr * record.probability / 100
            )
