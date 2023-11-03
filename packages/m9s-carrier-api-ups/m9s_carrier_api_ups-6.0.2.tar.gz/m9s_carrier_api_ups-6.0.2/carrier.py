# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.cache import Cache
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction


class Carrier(metaclass=PoolMeta):
    __name__ = 'carrier'

    # Provide a short lived cache for immediately
    # repeated requests to the API
    _ups_rate_cache = Cache('carrier_api_ups.rate',
        context=False, duration=10)

    @classmethod
    def __setup__(cls):
        super().__setup__()
        selection = ('api_ups', 'UPS API')
        if selection not in cls.carrier_cost_method.selection:
            cls.carrier_cost_method.selection.append(selection)

    def _get_rate(self):
        pool = Pool()
        Sale = pool.get('sale.sale')

        rate = self.__class__._ups_rate_cache.get(None, -1)
        if rate == -1:
            transaction = Transaction()
            sale = Sale(transaction.context['sale'])
            with transaction.set_context(ups_rate_api_mode='Rate'):
                rate = sale.get_shipping_rate(self)
                self.__class__._ups_rate_cache.set(None, rate)
        return rate

    def get_sale_price(self):
        if self.carrier_cost_method == 'api_ups':
            rate = self._get_rate()[0]
            return rate['cost'], rate['cost_currency'].id
        return super().get_sale_price()

    def get_purchase_price(self):
        if self.carrier_cost_method == 'api_ups':
            return self.get_sale_price()
        return super().get_purchase_price()


class CredentialUPS(metaclass=PoolMeta):
    __name__ = 'carrier.credential.ups'

    def get_shipment_url(self):
        api_mode = Transaction().context.get('ups_rate_api_mode')
        if api_mode == 'Shop':
            if self.server == 'production':
                return 'https://onlinetools.ups.com/api/rating/v1/shop'
            else:
                return 'https://wwwcie.ups.com/api/rating/v1/shop'
        elif api_mode == 'Rate':
            if self.server == 'production':
                return 'https://onlinetools.ups.com/api/rating/v1/rate'
            else:
                return 'https://wwwcie.ups.com/api/rating/v1/rate'
        return super().get_shipment_url()
