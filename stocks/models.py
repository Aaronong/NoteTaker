from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db.models import Sum, F

import urllib2
import datetime
import time
import json

QUERY = "http://localhost:8080/query?id={}"
ORDER = "http://localhost:8080/order?id={}&side=sell&qty={}&price={}"
ORDER_DISCOUNT = 1
N = 5
FAILURE_TOLERANCE = -3
SUCCESS_TOLERANCE = 2

@python_2_unicode_compatible
class ParentOrder(models.Model):
    quantity = models.IntegerField(blank=False, default=1)
    stock_type = models.CharField(max_length=20)
    is_sell = models.BooleanField(blank=False, default=True)
    time_executed = models.DateTimeField(blank=False, auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    IN_PROGRESS = 'P'
    COMPLETED = 'C'
    FAILED = 'F'
    PAUSED = 'S'
    CANCELLED = 'X'
    STATUS_CHOICES = (
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
        (PAUSED, 'Paused'),
        (CANCELLED, 'Cancelled')    
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=IN_PROGRESS
    )

    progress = models.FloatField(blank=False, default=0.0)
    
    # checks if quantity is positive
    def is_valid(self):
        if self.quantity <= 0:
            return False
        else:
            return True

    def get_total_price_sold(self, children):
        total_price = (children.filter(is_successful=True).aggregate(total=Sum(F('price') * F('quantity'))))['total']
        if total_price is None:
            return 0.0
        else:
            return total_price

    def get_total_quantity_sold(self, children):
        total_quantity = (children.filter(is_successful=True).aggregate(Sum('quantity')))['quantity__sum']
        if total_quantity is None:
            return 0
        else:
            return total_quantity

    def get_stats(self, children):
        if len(children) == 0:
            return {'total_price': 0.0, 'total_quantity': 0, 'average_price': 0.0}
        
        total_price = self.get_total_price_sold(children)
        total_quantity = self.get_total_quantity_sold(children)
        if total_price == 0.0:
            return {'total_price': total_price, 'total_quantity': total_quantity, 'average_price': 0.0}
        else:
            return {'total_price': total_price, 'total_quantity': total_quantity, 'average_price': total_price/total_quantity}

    def update_progress(self):
        children = ChildOrder.objects.filter(parent_order__id=self.id)
        quantity_sold = self.get_total_quantity_sold(children)

        self.progress = (float(quantity_sold)/float(self.quantity)) * 100
        self.save()

    def verify_market_price(self, price_json):
        top_bid = price_json.get('top_bid')
        if top_bid is None:
            return False
        price = top_bid.get('price')
        if price is None:
            return False
        return True

    def query_market_price(self, number_of_tries=10):
        quote = json.loads(urllib2.urlopen(QUERY.format(self.id)).read())
        while not self.verify_market_price(quote):  # We failed to verify, the exchange simulator returned a bad response
            quote = json.loads(urllib2.urlopen(QUERY.format(self.id)).read())
            time.sleep(5)  # sleep 5 seconds before trying again
            number_of_tries -= 1
            if number_of_tries == 0:  # no tries left, we give up querying and selling
                return False
        price = float(quote['top_bid']['price'])
        print "Quoted at %s" % price
        return price

    def query_market_datetime(self, number_of_tries=10):
        quote = json.loads(urllib2.urlopen(QUERY.format(self.id)).read())
        # do we need this while loop?
        while not self.verify_market_price(quote):  # We failed to verify, the exchange simulator returned a bad response
            quote = json.loads(urllib2.urlopen(QUERY.format(self.id)).read())
            time.sleep(5)  # sleep 5 seconds before trying again
            number_of_tries -= 1
            if number_of_tries == 0:  # no tries left, we give up querying and selling
                return False
        d = quote['timestamp'] + " UTC" # add UTC since this is time zone returned by simulator
        FORMAT = '%Y-%m-%d %H:%M:%S.%f %Z'
        dt = datetime.datetime.strptime(d, FORMAT)
        return dt

    def execute_sell(self, quantity, price):
        url   = ORDER.format(self.id, quantity, price)
        response = urllib2.urlopen(url).read()
        if response == "":
            order = {
            u'timestamp': self.query_market_datetime(),
            u'qty': quantity, 
            u'side': u'sell', 
            u'avg_price': 0.0
            }
        else:
            order = json.loads(response)
        return order

    def create_child(self, order, attempted_price):
        if (order['avg_price'] == 0.0):
            co = ChildOrder.objects.create(
                parent_order=self, 
                quantity = order['qty'],
                is_successful=False, 
                price=attempted_price
            )
        else:
            co = ChildOrder.objects.create(
                parent_order=self, 
                quantity = order['qty'],
                is_successful=True, 
                price=order['avg_price']
            )
            self.progress += (order['qty']/self.quantity) * 100
            self.save()

        co.time_executed = order['timestamp']
        co.save()
        return co

    def determine_quantity_to_sell(self):
        successful_children = ChildOrder.objects.filter(parent_order=self.id).filter(is_successful=True)
        quantity_sold_so_far = 0
        for child in successful_children:
            quantity_sold_so_far += child.quantity
        quantity_left_to_sell = self.quantity - quantity_sold_so_far
        return quantity_left_to_sell

    def trade(self):
        if not self.is_valid():
            print "Problem, someone created a bad parent order that shouldn't even be here"
            return  # This code should never be reached, since if an order is not valid, we don't even create it

        number_of_successes = 0
        if ((self.quantity/10) < 10):
            maximum_child_size = self.quantity
        else:
            maximum_child_size = self.quantity / 10  # hardcoded to split by 10%
        child_order_size = maximum_child_size
        quantity_to_sell = self.determine_quantity_to_sell()

        while quantity_to_sell > 0:
            price = self.query_market_price()
            if price is False:
                self.status = self.FAILED
                self.save()
                return
            price -= ORDER_DISCOUNT  # query is successful, update price accordingly
            if (quantity_to_sell < child_order_size):
                child_order_size = quantity_to_sell  # make sure child order size never exceeds what we have left to sell

            self.refresh_from_db()  # refresh before checking if paused or cancelled
            if (self.status == self.PAUSED or self.status == self.CANCELLED):
                return
                
            order = self.execute_sell(child_order_size, price)
            self.create_child(order, price)

            # logic for handling failure to sell
            if (order['avg_price'] == 0.0):
                number_of_successes -= 1
            else:
                number_of_successes += 1
                # update quantity if successful
                quantity_to_sell -= order['qty']
            
            # Divide child order quantity into smaller chunks if
            # we hit the failure tolerance
            if (number_of_successes == FAILURE_TOLERANCE):
                child_order_size /= 2
                number_of_successes = 0
            # If child order succeeds at smaller quantities, sell
            # at a higher quantity
            elif (number_of_successes == SUCCESS_TOLERANCE and child_order_size < maximum_child_size):
                child_order_size *= 2
                number_of_successes = 0

            # sleep for N seconds before selling again
            time.sleep(N)

        # DONE with while loop!
        self.status = self.COMPLETED
        self.save() # we forgot to save after setting self.success=True. The update() function solves this

    def __str__(self):
        return str(self.id) + ": " + str(self.quantity) + " x " + self.stock_type + ' status:' + self.status

@python_2_unicode_compatible
class ChildOrder(models.Model):
    parent_order = models.ForeignKey(ParentOrder, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, default=0)
    is_successful = models.BooleanField(blank=False, default=False)
    price = models.FloatField(blank=False, default=0.0)
    time_executed = models.DateTimeField(blank=False, auto_now_add=True)

    def __str__(self):
        return "id: " + str(self.id) + " quantity: " + str(self.quantity) + " price: " + str(self.price) + " successful? " + str(self.is_successful)
