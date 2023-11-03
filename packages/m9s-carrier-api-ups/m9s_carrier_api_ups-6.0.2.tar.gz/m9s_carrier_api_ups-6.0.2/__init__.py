# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool

from . import carrier, sale

__all__ = ['register']


def register():
    Pool.register(
        carrier.Carrier,
        carrier.CredentialUPS,
        sale.Sale,
        module='carrier_api_ups', type_='model')
    Pool.register(
        sale.ApplyShipping,
        sale.GetRateUPS,
        module='carrier_api_ups', type_='wizard')
    Pool.register(
        module='carrier_api_ups', type_='report')
