import base64
import logging

from odoo import api, fields, models
from odoo.tools import float_repr

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends(
        'amount_total_signed', 'amount_tax_signed', 'l10n_sa_confirmation_datetime',
        'company_id', 'company_id.vat',
        'journal_id', 'journal_id.l10n_sa_production_csid_json',
        'edi_document_ids', 'l10n_sa_invoice_signature', 'l10n_sa_chain_index', 'state',
    )
    def _compute_qr_code_str(self):
        """
        Wrap the l10n_sa_edi QR computation with error handling.

        For B2B (standard) invoices the parent extracts the QR code from the ZATCA-cleared
        XML attachment via an XPath lookup.  If ZATCA's sandbox response does not embed the
        QR node, or the node text is None/empty, the XPath raises IndexError (or produces a
        falsy result) and the field is left blank — causing the QR to vanish from the PDF.

        We catch both failure modes and fall back to the 5-field Phase-1 QR that is always
        derivable from the invoice's own fields (seller name, VAT, timestamp, total, tax).
        """
        try:
            super()._compute_qr_code_str()
        except Exception:
            _logger.warning(
                "ZATCA QR extraction raised an exception for moves %s; "
                "generating Phase-1 QR fallback for all.",
                self.mapped('name'),
            )
            for move in self:
                move.l10n_sa_qr_code_str = move._markition_phase1_qr()
            return

        # super() succeeded but some Phase-2 B2B invoices may still have an empty QR
        # (qr_node.text was None, or the QR node was absent without raising).
        for move in self:
            if (
                not move.l10n_sa_qr_code_str
                and move.country_code == 'SA'
                and move.state == 'posted'
                and move.l10n_sa_confirmation_datetime
                and move.company_id.vat
            ):
                move.l10n_sa_qr_code_str = move._markition_phase1_qr()

    def _markition_phase1_qr(self):
        """
        Generate the 5-field Phase-1 ZATCA QR (TLV-encoded, base64) from the invoice's
        own fields.  This is always available for any posted SA invoice with a VAT number
        and a confirmation datetime, regardless of Phase-2 clearance state.
        """
        self.ensure_one()

        def _tlv(tag, value_str):
            encoded = value_str.encode()
            return tag.to_bytes(1, 'big') + len(encoded).to_bytes(1, 'big') + encoded

        if not self.l10n_sa_confirmation_datetime or not self.company_id.vat:
            return ''

        time_sa = fields.Datetime.context_timestamp(
            self.with_context(tz='Asia/Riyadh'),
            self.l10n_sa_confirmation_datetime,
        )

        payload = (
            _tlv(1, self.company_id.display_name)
            + _tlv(2, self.company_id.vat)
            + _tlv(3, time_sa.strftime('%Y-%m-%dT%H:%M:%S'))
            + _tlv(4, float_repr(abs(self.amount_total_signed), 2))
            + _tlv(5, float_repr(abs(self.amount_tax_signed), 2))
        )
        return base64.b64encode(payload).decode()
