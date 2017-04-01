import six, mock, time

from django.test import TestCase
from models import User, ParentOrder, ChildOrder

from mock import MagicMock


class ParentOrderTestCase(TestCase):
    def setUp(self):
        u = User.objects.create(username="LIN",password='linisawesome')
        ParentOrder.objects.create(stock_type="ACME", is_sell=True, quantity=1000, user=u)
        ParentOrder.objects.create(stock_type="negative", is_sell=True, quantity=-1, user=u)  # broken case, negative numbers not allowed
        ParentOrder.objects.create(stock_type="zero", is_sell=True, quantity=0, user=u)  # broken case, negative numbers not allowed
        ParentOrder.objects.create(stock_type="small", is_sell=True, quantity=1, user=u)  # broken case, negative numbers not allowed


    def test_order_quantity_is_positive_number(self):
        working_order = ParentOrder.objects.get(stock_type="ACME")
        negative_order = ParentOrder.objects.get(stock_type="negative")
        zero_order = ParentOrder.objects.get(stock_type="zero")
        self.assertTrue(working_order.is_valid())
        self.assertFalse(negative_order.is_valid())
        self.assertFalse(zero_order.is_valid())

    def parent_order_fails_correctly_if_exchange_simulator_returns_bad_response(self):
        working_order = ParentOrder.objects.get(stock_type="ACME")
        working_order.query_market_price = MagicMock(return_value=False)  # intentionally cause query_market_price to fail
        self.assertEqual(working_order.status, working_order.IN_PROGRESS) 
        working_order.trade()
        time.sleep(5)
        self.assertEqual(working_order.status, working_order.FAILED)  # This should be FAILED

    def parent_order_can_handle_small_input_quantity_and_create_children(self):
        '''
        We expect to sell with a quantity of 1. We need to set status=COMPLETED and create a child in the database
        '''
        small_order = ParentOrder.objects.get(stock_type="small")
        small_order.create_child = MagicMock()
        small_order.query_market_price = MagicMock(return_value=100)  # arbitrary price
        fake_order = {'avg_price': 100, 'qty': 1}  # what we expect an order JSON to look like when returned from exchange simulator
        small_order.execute_sell = MagicMock(return_value=fake_order)
        self.assertEqual(small_order.status, small_order.IN_PROGRESS)
        small_order.trade()
        time.sleep(5)
        self.assertEqual(small_order.status, small_order.COMPLETED)
        small_order.create_child.assert_called_once_with(fake_order, 90) # 90 here because price = market_price - 10
        # successfully created a child

    def parent_order_can_pause_and_resume(self):
        return True
