from lxml import etree

from odoo import api, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.model
    def get_views(self, views, options=None):
        ret_val = super().get_views(views, options)

        form_view = self.env["ir.ui.view"].browse(ret_val["views"]["form"]["id"])
        if form_view.xml_id != "base.res_config_settings_view_form":
            return ret_val

        doc = etree.XML(ret_val["views"]["form"]["arch"])

        for item in doc.xpath("//setting[field[@widget='upgrade_boolean']]"):
            item.attrib["class"] = "d-none"

        for block in doc.xpath("//block"):
            visible = block.xpath(
                "setting[not(contains(@class,'d-none')) and not(@invisible='1')]"
            )
            if not visible:
                block.attrib.pop("title", None)
                block.attrib.pop("tip", None)
                block.attrib["class"] = "d-none"

        ret_val["views"]["form"]["arch"] = etree.tostring(doc)
        return ret_val
