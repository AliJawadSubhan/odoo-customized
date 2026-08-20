from odoo.tools import config


def post_init_hook(env):
    # Disable template override when running tests so other modules' tests
    # that depend on the original brand_promotion_message structure still pass.
    if config["test_enable"] or config["test_file"]:
        env.ref(
            "markition_website_debranding.layout_footer_copyright"
        ).active = False
