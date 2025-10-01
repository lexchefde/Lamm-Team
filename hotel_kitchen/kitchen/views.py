from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Supplier

class SupplierListView(ListView):
    model = Supplier
    template_name = 'kitchen/supplier_list.html'
    context_object_name = 'suppliers'

class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'kitchen/supplier_detail.html'
    context_object_name = 'supplier'

class SupplierCreateView(CreateView):
    model = Supplier
    template_name = 'kitchen/supplier_form.html'
    fields = ['name', 'contact_person', 'email', 'phone_number', 'address', 'delivery_notes']
    success_url = reverse_lazy('kitchen:supplier_list')

class SupplierUpdateView(UpdateView):
    model = Supplier
    template_name = 'kitchen/supplier_form.html'
    fields = ['name', 'contact_person', 'email', 'phone_number', 'address', 'delivery_notes']
    success_url = reverse_lazy('kitchen:supplier_list')

class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = 'kitchen/supplier_confirm_delete.html'
    success_url = reverse_lazy('kitchen:supplier_list')