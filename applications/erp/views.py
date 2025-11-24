from django.views.generic import TemplateView, DetailView, ListView, UpdateView, CreateView
from django.db.models import Q, Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages

# 🔹 Modelos
from .models import Client, Budget, BudgetItem
from applications.erp.models import CompanyInfo  # ✅ Import correcto

# 🔹 Formularios
from .forms import BudgetForm, BudgetItemFormSet, ClientForm

# ===============================
# DASHBOARD
# ===============================
class DashboardView(UserPassesTestMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 📊 Datos generales
        context['total_clientes'] = Client.objects.count()
        context['lista_clientes'] = Client.objects.all()
        context['total_facturas'] = Budget.objects.count()
        context['total_presupuesto_monto'] = Budget.objects.aggregate(Sum('total'))['total__sum'] or 0

        # 📊 Gráficos por semana
        clients_weekly = Client.objects.extra({'created_week': "strftime('%%W', date_joined)"}).values('created_week').annotate(count=Count('id')).order_by('created_week')
        budgets_weekly = Budget.objects.extra({'created_week': "strftime('%%W', fecha_creacion)"}).values('created_week').annotate(count=Count('id')).order_by('created_week')

        # 📊 Gráficos por mes
        clients_monthly = Client.objects.extra({'created_month': "strftime('%%m', date_joined)"}).values('created_month').annotate(count=Count('id')).order_by('created_month')
        budgets_monthly = Budget.objects.extra({'created_month': "strftime('%%m', fecha_creacion)"}).values('created_month').annotate(count=Count('id')).order_by('created_month')

        # 🔹 Enviar datos al template
        context['chart_data_week_clients'] = [data['count'] for data in clients_weekly]
        context['chart_data_week_budgets'] = [data['count'] for data in budgets_weekly]
        context['chart_data_month_clients'] = [data['count'] for data in clients_monthly]
        context['chart_data_month_budgets'] = [data['count'] for data in budgets_monthly]

        return context

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "Solo el equipo staff puede acceder a esta página.")
        return redirect("home_app:home")


# ===============================
# CREAR PRESUPUESTO
# ===============================
class BudgetCreateView(CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'dashboard/presupuesto.html'
    success_url = reverse_lazy('dashboard_app:budget_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = BudgetItemFormSet(self.request.POST)
        else:
            context['item_formset'] = BudgetItemFormSet(queryset=BudgetItem.objects.none())
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']

        if item_formset.is_valid():
            self.object = form.save()

            item_formset.instance = self.object
            item_formset.save()

            self.object.total = self.object.calcular_total_con_impuestos
            self.object.save()

            return redirect('dashboard_app:budget_detail', pk=self.object.id)
        return self.form_invalid(form)


# ===============================
# ACTUALIZAR ÍTEM DE PRESUPUESTO
# ===============================
def delete_budget_item(request, item_id):
    item = get_object_or_404(BudgetItem, id=item_id)
    item.delete()
    return redirect('create_budget')


# ===============================
# AÑADIR CLIENTE
# ===============================
def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_app:create_budget')
    else:
        form = ClientForm()

    clientes = Client.objects.all()

    return render(request, 'dashboard/add_client.html', {
        'form': form,
        'clientes': clientes
    })


# ===============================
# CONFIRMACIÓN TRAS CREAR PRESUPUESTO
# ===============================
def budget_success(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    return redirect('dashboard_app:budget_detail', pk=budget.id)


# ===============================
# EDITAR PRESUPUESTO
# ===============================
class BudgetUpdateView(UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = "dashboard/budget_form.html"
    success_url = reverse_lazy('dashboard_app:budget_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = BudgetItemFormSet(self.request.POST, instance=self.object)
        else:
            context['item_formset'] = BudgetItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']

        if form.is_valid() and item_formset.is_valid():
            self.object = form.save()

            items = item_formset.save(commit=False)
            for item in items:
                item.presupuesto = self.object
                item.save()

            for deleted_item in item_formset.deleted_objects:
                deleted_item.delete()

            total = sum(item.subtotal for item in self.object.items.all())
            self.object.total = total
            self.object.save()

            return super().form_valid(form)

        return self.form_invalid(form)


# ===============================
# LISTAR PRESUPUESTOS
# ===============================
class BudgetListView(ListView):
    model = Budget
    template_name = "dashboard/budget_list.html"
    context_object_name = "budgets"

    def get_queryset(self):
        queryset = super().get_queryset().exclude(id__isnull=True)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(cliente__nombre__icontains=query) |
                Q(id__iexact=query)
            )
        return queryset.order_by('-id')


# ===============================
# VER DETALLE DE PRESUPUESTO
# 🔹 Aquí agregamos CompanyInfo correctamente
# ===============================
class BudgetDetailView(DetailView):
    model = Budget
    template_name = "dashboard/budget_detail.html"
    context_object_name = "budget"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        budget = self.get_object()

        context["company"] = CompanyInfo.objects.first()  # ✅ AÑADIDO

        context["subtotal"] = budget.calcular_subtotal
        context["impuestos"] = budget.calcular_impuestos
        context["total_con_impuestos"] = budget.calcular_total_con_impuestos
        context["items"] = budget.items.all()
        return context
