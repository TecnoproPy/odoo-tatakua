# For copyright and license notices, see __manifest__.py file in module root

from openupgradelib import openupgrade
import logging

_logger = logging.getLogger(__name__)


@openupgrade.migrate()
def migrate(env, version):

    _logger.info('Migration -> poner partner type en clientes locales')
    env.cr.execute("""
    UPDATE res_partner
    SET partner_type_sale_id = partner_type_id;
    """)
