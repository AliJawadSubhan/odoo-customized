import threading
import werkzeug.routing

from odoo import models, tools
from odoo.addons.base.models.ir_http import _logger, FasterRule
from odoo.http import ROUTING_KEYS
from odoo.tools.misc import submap
from odoo.modules.registry import Registry
import odoo

# Per-database sorturl cache: {dbname: sorturl_string}
# Written by routing_map() when a database's routing map is built.
# Read by JavascriptAsset.content (see __init__.py) for JS rewriting.
# Keyed by database name — no cross-database contamination.
_db_sorturls = {}


class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    def write(self, vals):
        result = super().write(vals)
        if result and self.key == 'web.base.sorturl':
            self.env['ir.http'].env.registry.clear_cache("routing")
            self.env['ir.attachment'].regenerate_assets_bundles()
            return {'type': 'ir.actions.client', 'tag': 'soft_reload'}
        return result


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @tools.ormcache('key', cache='routing')
    def routing_map(self, key=None):
        config_parameter = self.env['ir.config_parameter']
        sorturl = config_parameter.sudo().get_param("web.base.sorturl", "")

        dbname = threading.current_thread().dbname
        _db_sorturls[dbname] = sorturl

        _logger.info("Generating routing map for key %s", str(key))
        registry = Registry(dbname)
        installed = registry._init_modules.union(
            odoo.tools.config['server_wide_modules'])
        mods = sorted(installed)
        routing_map = werkzeug.routing.Map(
            strict_slashes=False, converters=self._get_converters())
        for url, endpoint in self._generate_routing_rules(
                mods, converters=self._get_converters()):
            routing = submap(endpoint.routing, ROUTING_KEYS)
            if routing['methods'] is not None and 'OPTIONS' not in routing['methods']:
                routing['methods'] = routing['methods'] + ['OPTIONS']
            # Always register the original route (e.g. /odoo, /odoo/<path>)
            rule = FasterRule(url, endpoint=endpoint, **routing)
            rule.merge_slashes = False
            routing_map.add(rule)
            # Also register the custom URL alias (e.g. /markition-erp)
            if sorturl and 'odoo' in url:
                custom_url = url.replace('odoo', sorturl)
                custom_rule = FasterRule(custom_url, endpoint=endpoint, **routing)
                custom_rule.merge_slashes = False
                routing_map.add(custom_rule)
        return routing_map
