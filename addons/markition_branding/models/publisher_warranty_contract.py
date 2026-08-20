from odoo import models
from odoo.release import version_info


class PublisherWarrantyContract(models.AbstractModel):
    _inherit = "publisher_warranty.contract"

    def update_notification(self, cron_mode=True):
        # Suppress update pings on Community (non-Enterprise) installs.
        if version_info[5] == "e":
            return super().update_notification(cron_mode=cron_mode)
        return True
