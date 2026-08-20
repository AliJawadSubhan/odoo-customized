import re

from lxml import etree, html
from markupsafe import Markup

from odoo import api, models


class MailRenderMixin(models.AbstractModel):
    _inherit = "mail.render.mixin"

    def remove_href_odoo(self, value, to_keep=None):
        """Strip <a href="...odoo.com..."> links (and their surrounding text)
        from rendered HTML. Leaves dev.odoo.com links intact so internal
        debug/developer tools keep working."""
        if len(value) < 20:
            return value
        back_to_bytes = False
        back_to_markup = False
        if isinstance(value, bytes):
            back_to_bytes = True
            value = value.decode()
        if isinstance(value, Markup):
            back_to_markup = True
        has_dev_odoo_link = re.search(
            r"<a\s(.*)dev\.odoo\.com", value, flags=re.IGNORECASE
        )
        has_odoo_link = re.search(r"<a\s(.*)odoo\.com", value, flags=re.IGNORECASE)
        if has_odoo_link and not has_dev_odoo_link:
            if to_keep:
                value = value.replace(to_keep, "<body_msg></body_msg>")
            tree = html.fromstring(value)
            for elem in tree.xpath('//a[contains(@href,"odoo.com")]'):
                parent = elem.getparent()
                previous = elem.getprevious()
                if previous is not None:
                    previous.tail = etree.CDATA("&nbsp;")
                elif parent.text:
                    parent.text = etree.CDATA("&nbsp;")
                parent.remove(elem)
            value = etree.tostring(
                tree, pretty_print=True, method="html", encoding="unicode"
            )
            if to_keep:
                value = value.replace("<body_msg></body_msg>", to_keep)
        if back_to_bytes:
            value = value.encode()
        elif back_to_markup:
            value = Markup(value)
        return value

    @api.model
    def _render_template(
        self,
        template_src,
        model,
        res_ids,
        engine="inline_template",
        add_context=None,
        options=None,
    ):
        rendered = super()._render_template(
            template_src,
            model,
            res_ids,
            engine=engine,
            add_context=add_context,
            options=options,
        )
        for key in res_ids:
            rendered[key] = self.remove_href_odoo(rendered[key])
        return rendered
