import re
import threading

from odoo.addons.base.models.assetsbundle import JavascriptAsset
from odoo.tools.js_transpiler import transpile_javascript

from . import models
from .models.home import _db_sorturls

# Save the original before patching so _uninstall_cleanup can restore it exactly.
_original_js_content = JavascriptAsset.content


@property
def _patched_js_content(self):
    content = super(JavascriptAsset, self).content
    _needs_rewrite = self.name in (
        "/web/static/src/core/browser/router.js",
        "/web/static/src/webclient/navbar/navbar.js",
    )
    if _needs_rewrite:
        dbname = getattr(threading.current_thread(), 'dbname', None)
        sorturl = _db_sorturls.get(dbname, '') if dbname else ''
        if sorturl:
            content = re.sub(r'(?<!@)odoo', sorturl, content)
            self._converted_content = None
    if self.is_transpiled:
        if not self._converted_content:
            self._converted_content = transpile_javascript(self.url, content)
        return self._converted_content
    return content


JavascriptAsset.content = _patched_js_content


def _uninstall_cleanup(env):
    JavascriptAsset.content = _original_js_content
    env['ir.http'].env.registry.clear_cache("routing")
    env['ir.attachment'].regenerate_assets_bundles()
