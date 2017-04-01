from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


@python_2_unicode_compatible
class NoteUser(User):

    def __str__(self):
        return self.username

    # needs tagging and authorizing functions, also view all notebooks, docs, tags, search notes
    # view should be conditional, allowing additional functions depending on permission
    # create new notebook, doc, note


@python_2_unicode_compatible
class Notebook(models.Model):
    owner = models.ForeignKey(NoteUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    # view all docs


@python_2_unicode_compatible
class Document(models.Model):
    title = models.CharField(max_length=50)
    notebook = models.ForeignKey(Notebook) # reparented to diff notebook upon delete
    permissions = models.ManyToManyField(
        NoteUser,
        through='Authorization',
        through_fields= ('document', 'user')
    )
    time_created = models.DateTimeField(blank=False, auto_now_add=True)
    time_modified = models.DateTimeField(blank=False, auto_now_add=True)

    def __str__(self):
        return self.title

    # view all notes, all permissions for author, collaborators for everyone else


@python_2_unicode_compatible
class Authorization(models.Model):
    user = models.ForeignKey(NoteUser, on_delete=models.CASCADE)
    type = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(3)])
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    initiator = models.ForeignKey(
        NoteUser,
        on_delete=models.CASCADE,
        related_name="authorizing",
    )

    def __str__(self):
        choice_text = ['read', 'comment', 'write', 'author'][self.type]
        return self.user.__str__() + " is authorized to " + choice_text + " " + self.document.__str__()


@python_2_unicode_compatible
class Note(models.Model):
    author = models.ForeignKey(NoteUser, on_delete=models.CASCADE)
    note_text = models.CharField(max_length=5000)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    time_created = models.DateTimeField(blank=False, auto_now_add=True)
    time_modified = models.DateTimeField(blank=False, auto_now_add=True)

    def __str__(self):
        return "Note of id " + str(self.pk)

    # view all tags, comments, author gets permissions button


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

    def __str__(self):
        return self.note.__str__() + " has the tag " + self.tag.__str__()


@python_2_unicode_compatible
class Comment(models.Model):
    author = models.ForeignKey(NoteUser, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return "This should not show"


@python_2_unicode_compatible
class InsertComment(Comment):
    text = models.CharField(max_length=500)
    insert_position = models.IntegerField(blank=False)

    def __str__(self):
        return "Text insertion by", self.author, "for", self.note

@python_2_unicode_compatible
class DeleteComment(Comment):
    delete_start = models.IntegerField(blank=False)
    delete_end = models.IntegerField(blank=False)

    def __str__(self):
        return "Text deletion by", self.author, "for", self.note


@python_2_unicode_compatible
class TextComment(Comment):
    text = models.CharField(max_length=500)
    comment_position = models.IntegerField(blank=False)

    def __str__(self):
        return "Comment by", self.author, "for", self.note


# # Create your models here.
# @python_2_unicode_compatible
# class ChildOrder(models.Model):
#     parent_order = models.ForeignKey(ParentOrder, on_delete=models.CASCADE)
#     quantity = models.IntegerField(blank=False, default=0)
#     is_successful = models.BooleanField(blank=False, default=False)
#     price = models.FloatField(blank=False, default=0.0)
#     time_executed = models.DateTimeField(blank=False, auto_now_add=True)
#
#     def __str__(self):
#         return "id: " + str(self.id) + " quantity: " + str(self.quantity) + " price: " + str(self.price) + " successful? " + str(self.is_successful)
#
#
# @python_2_unicode_compatible
# class ParentOrder(models.Model):
#     quantity = models.IntegerField(blank=False, default=1)
#     stock_type = models.CharField(max_length=20)
#     is_sell = models.BooleanField(blank=False, default=True)
#     time_executed = models.DateTimeField(blank=False, auto_now_add=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     IN_PROGRESS = 'P'
#     COMPLETED = 'C'
#     FAILED = 'F'
#     PAUSED = 'S'
#     CANCELLED = 'X'
#     STATUS_CHOICES = (
#         (IN_PROGRESS, 'In Progress'),
#         (COMPLETED, 'Completed'),
#         (FAILED, 'Failed'),
#         (PAUSED, 'Paused'),
#         (CANCELLED, 'Cancelled')
#     )
#
#     status = models.CharField(
#         max_length=1,
#         choices=STATUS_CHOICES,
#         default=IN_PROGRESS
#     )
#
#     progress = models.FloatField(blank=False, default=0.0)
#
#     # checks if quantity is positive
#     def is_valid(self):
#         if self.quantity <= 0:
#             return False
#         else:
#             return True
#
#     def get_total_price_sold(self, children):
#         total_price = (children.filter(is_successful=True).aggregate(total=Sum(F('price') * F('quantity'))))['total']
#         if total_price is None:
#             return 0.0
#         else:
#             return total_price
#
#     successful_children = ChildOrder.objects.filter(parent_order=self.id).filter(is_successful=True)
#
#     def create_child(self, order, attempted_price):
#         if (order['avg_price'] == 0.0):
#             co = ChildOrder.objects.create(
#                 parent_order=self,
#                 quantity = order['qty'],
#                 is_successful=False,
#                 price=attempted_price
#             )
#         else:
#             co = ChildOrder.objects.create(
#                 parent_order=self,
#                 quantity = order['qty'],
#                 is_successful=True,
#                 price=order['avg_price']
#             )
#             self.progress += (order['qty']/self.quantity) * 100
#             self.save()
#
#         co.time_executed = order['timestamp']
#         co.save()
#         return co