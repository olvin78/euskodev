from django.views.generic import TemplateView, DetailView, ListView, UpdateView, CreateView
from django.db.models import Q, Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST

# 🔹 Importar modelos
from .models import Client, Budget, BudgetItem
from applications.erp.models import CompanyInfo  # Import correcto

# 🔹 Formularios
from .forms import BudgetForm, BudgetItemFormSet, ClientForm


# ===============================
# DASHBOARD
# ===============================
class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "Solo el equipo staff puede acceder.")
        return redirect("home_app:home")


class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_clientes'] = Client.objects.count()
        context['lista_clientes'] = Client.objects.all()
        context['total_presupuestos'] = Budget.objects.count()
        context['total_presupuesto_monto'] = Budget.objects.aggregate(Sum('total'))['total__sum'] or 0

        return context

# ===============================
# CREAR PRESUPUESTO
# ===============================
class BudgetCreateView(StaffRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'dashboard/presupuesto.html'
    success_url = reverse_lazy('dashboard_app:budget_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_formset'] = BudgetItemFormSet(self.request.POST or None)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']

        if item_formset.is_valid():
            self.object = form.save()  # Guardar presupuesto
            item_formset.instance = self.object
            item_formset.save()  # Guardar ítems

            self.object.update_totals()  # 🔹 Recalcular totales

            return redirect('dashboard_app:budget_detail', pk=self.object.id)
        return self.form_invalid(form)


# ===============================
# ACTUALIZAR PRESUPUESTO
# ===============================
class BudgetUpdateView(StaffRequiredMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = "dashboard/budget_form.html"
    success_url = reverse_lazy('dashboard_app:budget_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_formset'] = BudgetItemFormSet(self.request.POST or None, instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']

        if item_formset.is_valid():
            self.object = form.save()
            item_formset.save()

            self.object.update_totals()  # 🔹 Recalcular totales

            return super().form_valid(form)
        return self.form_invalid(form)


# ===============================
# LISTAR PRESUPUESTOS
# ===============================
class BudgetListView(StaffRequiredMixin, ListView):
    model = Budget
    template_name = "dashboard/budget_list.html"
    context_object_name = "budgets"

    def get_queryset(self):
        queryset = Budget.objects.select_related('cliente').all().order_by('-id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(cliente__nombre__icontains=query) |
                Q(numero_presupuesto_manual__icontains=query)
            )
        return queryset


# ===============================
# VER DETALLE DE PRESUPUESTO
# ===============================
class BudgetDetailView(StaffRequiredMixin, DetailView):
    model = Budget
    template_name = "dashboard/budget_detail.html"
    context_object_name = "budget"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budget = self.get_object()

        # 🔹 Datos adicionales
        context["company"] = CompanyInfo.objects.first()
        context["items"] = budget.items.all()
        context["subtotal"] = budget.calcular_subtotal
        context["impuestos"] = budget.calcular_impuestos
        context["total_con_impuestos"] = budget.calcular_total_con_impuestos

        return context


# ===============================
# AÑADIR CLIENTE DESDE PRESUPUESTO
# ===============================
@login_required
@user_passes_test(lambda user: user.is_staff)
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente creado correctamente.")
            return redirect('dashboard_app:create_budget')
    else:
        form = ClientForm()

    return render(request, 'dashboard/add_client.html', {'form': form})


# ===============================
# ELIMINAR ÍTEM DE PRESUPUESTO
# ===============================
@login_required
@user_passes_test(lambda user: user.is_staff)
@require_POST
def delete_budget_item(request, item_id):
    item = get_object_or_404(BudgetItem, id=item_id)
    budget_id = item.presupuesto.id
    item.delete()
    messages.success(request, "Ítem eliminado correctamente.")
    return redirect('dashboard_app:update_budget', pk=budget_id)
