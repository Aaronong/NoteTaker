from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db import models


@python_2_unicode_compatible
class NoteUser(models.Model):
    alias = models.OneToOneField(User)


@python_2_unicode_compatible
class Tags(models.Model):
    tag_text = models.CharField(max_length=20)
    note_ids = models.ManyToManyField(
        Note,
        through='Tagging',
        through_fields=('tag','note')
    )

    def __str__(self):
        return self.tag_text


@python_2_unicode_compatible
class Tagging(models.Model):
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    initiator = models.ForeignKey(
        NoteUser,
        on_delete=models.CASCADE,
        related_name="tagging",
    )

@python_2_unicode_compatible
class Note(models.Model):
    author = models.ForeignKey(NoteUser, on_delete=models.CASCADE)


@python_2_unicode_compatible
class Document(models.Model):
    author = models.ForeignKey(NoteUser, on_delete=models.CASCADE)


@python_2_unicode_compatible
class Comment(models.Model):
    author = models.ForeignKey(NoteUser, on_delete=models.CASCADE)


@python_2_unicode_compatible
class InsertComment(Comment):
    pass


@python_2_unicode_compatible
class DeleteComment(Comment):
    pass


@python_2_unicode_compatible
class TextComment(Comment):
    pass


# Create your models here.
@python_2_unicode_compatible
class ChildOrder(models.Model):
    parent_order = models.ForeignKey(ParentOrder, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, default=0)
    is_successful = models.BooleanField(blank=False, default=False)
    price = models.FloatField(blank=False, default=0.0)
    time_executed = models.DateTimeField(blank=False, auto_now_add=True)

    def __str__(self):
        return "id: " + str(self.id) + " quantity: " + str(self.quantity) + " price: " + str(self.price) + " successful? " + str(self.is_successful)


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
