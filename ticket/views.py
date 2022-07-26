from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin
from guardian.shortcuts import get_objects_for_user
from .models import Ticket, Replie


@login_required
def home(request):
	context = {
		'tickets': Ticket.objects.all()
	}
	return render(request, 'ticket/home.html', context)


class TicketListView(LoginRequiredMixin, ListView):
	model = Ticket
	template_name = 'ticket/home.html'
	context_object_name = 'tickets'
	paginate_by = 5

	def get_queryset(self):
		return Ticket.objects.order_by('-urgency', '-date_ticketed').order_by('-urgency')

class FilterListView(LoginRequiredMixin, ListView):
	model = Ticket
	template_name = 'ticket/user_tickets.html'
	context_object_name = 'tickets'
	paginate_by = 5
	ordering = ['-urgency', '-date_ticketed']

	def get_queryset(self):  
		queryset = super().get_queryset()
		status = self.kwargs.get('status')
		if status:
			if self.request.user.has_perm("ticket.view_ticket"):
				queryset = queryset.filter(status=status).order_by('-urgency')
			else:
				queryset = queryset.filter(author=self.request.user, status=status).order_by('-urgency')
		else:
			if self.request.user.has_perm("ticket.view_ticket"):
				queryset = queryset.order_by('-urgency')
			else:
				queryset = queryset.filter(author=self.request.user).order_by('-urgency')
		return queryset

class UserTicketListView(LoginRequiredMixin, ListView):
	model = Ticket
	template_name = 'ticket/user_tickets.html'
	context_object_name = 'tickets'
	paginate_by = 5

	def get_queryset(self):
		queryset = super().get_queryset()
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		if self.request.user == user or self.request.user.has_perm("ticket.view_ticket"):
			queryset = Ticket.objects.filter(author=user).order_by('-urgency')
		else:
			raise PermissionDenied
		return queryset

class TicketDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
	model = Ticket
	permission_required = 'ticket.view_ticket'

class TicketCreateView(LoginRequiredMixin, CreateView):
	model = Ticket
	fields = ['title', 'ticket_type', 'urgency', 'content']

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class TicketReplieView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
	model = Replie
	template_name = 'ticket/add_replie.html'
	fields = ['body']
	raise_exception = False

	def form_valid(self,form):
		form.instance.replier = self.request.user
		form.instance.ticket_id = self.kwargs['pk']
		return super().form_valid(form)

	def test_func(self):
		ticket = get_object_or_404(Ticket, pk=self.kwargs['pk'])
		if self.request.user == ticket.author or self.request.user.is_staff:
			return True
		return False

class TicketUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	model = Ticket
	fields = ['title', 'urgency', 'content', 'status']
	permission_required = "ticket.change_ticket"
	
	def form_valid(self,form):
		return super().form_valid(form)


class TicketDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	model = Ticket
	success_url = '/'

	permission_required = "ticket.delete_ticket"