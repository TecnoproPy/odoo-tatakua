# For copyright and license notices, see __manifest__.py file in module root
import logging

_logger = logging.getLogger(__name__)

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):

    _logger.info('Migration -> Adding new column partner_type')
    env.cr.execute("""
    ALTER TABLE res_partner
    ADD COLUMN partner_type_id INTEGER;
    """)

    _logger.info('Migration -> Setting inital values for partner_type')
    env.cr.execute("""
    UPDATE res_partner SET partner_type_id = 1;
    """)
