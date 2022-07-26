from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from guardian.shortcuts import assign_perm



# Create your models here.
class Ticket(models.Model):
	urgency_choices = [
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5'),
		(6, '6'),
		(7, '7'),
		(8, '8'),
		(9, '9'),
		(10, '10'),
	]

	ticket_type_choices = [
        ('Service Request Ticket', 'Service Request Ticket'),
        ('Incident Ticket', 'Incident Ticket'),
        ('Problem Ticket', 'Problem Ticket'),
        ('Change Request Ticket', 'Change Request Ticket'),
    ]

	ticket_statuses = [
	    ('N', 'New'),
	    ('O', 'Open'),
	    ('W', 'Working'),
	    ('C', 'Closed'),
	]

	title = models.CharField(max_length=100)
	content = models.TextField()
	date_ticketed = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=1, choices=ticket_statuses, default='N')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	ticket_type = models.CharField(max_length=50, default='IT', choices=ticket_type_choices)
	urgency = models.IntegerField(
		default=1, 
		validators=[MinValueValidator(1), MaxValueValidator(10)], 
		verbose_name='Urgency (1-10)', 
		error_messages={'max_value': 'Please Choose an Urgency Between 1 and 10', 'min_value': 'Please Choose an Urgency Between 1 and 10'})

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('ticket-detail', kwargs={'pk': self.pk})

Ticket.objects.order_by('-urgency')

@receiver(post_save, sender=Ticket)
def set_permission(sender, instance, **kwargs):
	assign_perm("view_ticket", instance.author, instance)
	assign_perm("change_ticket", instance.author, instance)
	assign_perm("delete_ticket", instance.author, instance)
	group = Group.objects.get(name='Ticketing Staff')
	assign_perm("view_ticket", group, instance)
	assign_perm("change_ticket", group, instance)
	assign_perm("delete_ticket", group, instance)

class Replie(models.Model):
	ticket = models.ForeignKey(Ticket, related_name="replies", on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	replier = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField()
	date_replied = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return '%s - %s' % (self.ticket.title, self.name)

	def get_absolute_url(self):
		return reverse('ticket-home')