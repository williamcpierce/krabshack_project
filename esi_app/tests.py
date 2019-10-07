from django.test import TestCase
import esi_app.util as util
import json


with open('esi_app/test_lp.json') as test_lp:
    json_lp = json.load(test_lp)


with open('esi_app/test_orders.json') as test_orders:
    json_orders = json.load(test_orders)


with open('esi_app/test_history.json') as test_history:
    json_history = json.load(test_history)


class EsiRequestTestCase(TestCase):

    def test_orders_url(self):
        url = util.build_esi_url(
            op='orders',
            region_id=10000002,
            type_id=34,
            order_type='all'
        )
        self.assertEqual(url, 'https://esi.evetech.net/latest/markets/10000002/orders/?order_type=all&type_id=34')

    def test_history_url(self):
        url = util.build_esi_url(
            op='history',
            region_id=10000002,
            type_id=34,
        )
        self.assertEqual(url, 'https://esi.evetech.net/latest/markets/10000002/history/?type_id=34')

    def test_orders_response(self):
        response = util.esi_request(
            op='orders',
            region_id=10000002,
            type_id=34,
            order_type='all'
        )
        self.assertEqual(response.status_code, 200)

    def test_history_response(self):
        response = util.esi_request(
            op='history',
            region_id=10000002,
            type_id=34,
        )
        self.assertEqual(response.status_code, 200)


class ParsingTestCase(TestCase):

    def test_parse_lp(self):
        exists = util.parse_lp(json_lp, 1000005)
        notexist = util.parse_lp(json_lp, 2000005)
        self.assertEqual(exists, 24)
        self.assertEqual(notexist, 0)

    def test_parse_orders(self):
        parsed_orders = util.parse_market_orders(json_orders)
        sell_order_min = parsed_orders['sell_order_min']
        buy_order_max = parsed_orders['buy_order_max']
        self.assertEqual(sell_order_min, 6.33)
        self.assertEqual(buy_order_max, 5.63)

    def test_parse_history(self):
        volume = util.parse_market_history(json_history)
        self.assertEqual(volume, 6454700624.86)
