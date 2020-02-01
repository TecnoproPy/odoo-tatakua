# For copyright and license notices, see __manifest__.py file in module root
import logging

_logger = logging.getLogger(__name__)

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    _logger.info('Setting inital values for partner_type')
    env.cr.execute("""
    UPDATE res_partner SET partner_type_id = 1
    """)
