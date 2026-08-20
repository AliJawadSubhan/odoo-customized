import { registry } from "@web/core/registry";
// Import to ensure items are registered before we remove them.
import "@web/webclient/user_menu/user_menu_items";

registry.category("user_menuitems").remove("support");
registry.category("user_menuitems").remove("odoo_account");
