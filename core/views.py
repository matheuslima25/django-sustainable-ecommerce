from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DetailView, ListView,
                                  TemplateView, UpdateView)
from django.views.generic.edit import FormMixin

from .forms import BrandForm, ProductForm, ReviewForm
from .models import Brand, Product, Review, StockOut


class ProductListView(View):
    def get(self, request):
        search_query = request.GET.get('q', '')
        product_type = request.GET.get('type', '')
        gender = request.GET.get('gender', '')
        size = request.GET.get('size', '')
        page = request.GET.get('page', 1)

        products = Product.objects.all()
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | Q(code__icontains=search_query)
            )
        if product_type:
            products = products.filter(product_type=product_type)
        if gender:
            if gender in ['M', 'F']:
                products = products.filter(Q(gender=gender) | Q(gender='U'))
            else:
                products = products.filter(gender='U')
        if size:
            products = products.filter(
                Q(shoe_size=size) | Q(clothing_size=size)
            )

        paginator = Paginator(products, 6)  # 6 produtos por página
        products_page = paginator.get_page(page)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('core/includes/product_cards.html', {'products': products_page})
            return JsonResponse({'html': html})

        shoe_sizes = [str(i) for i in range(20, 45)]
        clothing_sizes = ['PP', 'P', 'M', 'G', 'GG']

        context = {
            'products': products_page,
            'search_query': search_query,
            'shoe_sizes': shoe_sizes,
            'clothing_sizes': clothing_sizes,
        }
        return render(request, 'core/product_list.html', context)


class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    template_name = 'core/product_form.html'
    success_url = reverse_lazy('core:product_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'core/product_form.html'
    success_url = reverse_lazy('core:product_list')


class ProductDetailView(FormMixin, DetailView):
    model = Product
    template_name = 'core/product_detail.html'
    context_object_name = 'product'
    form_class = ReviewForm

    def get_success_url(self):
        return reverse('core:product_detail', kwargs={'pk': self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            review = form.save(commit=False)
            review.product = self.object
            review.user = request.user
            review.save()
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Sugestões por tipo ou gênero (exclui o próprio)
        context['suggested'] = Product.objects.filter(
            Q(product_type=product.product_type) | Q(gender=product.gender)
        ).exclude(id=product.id)[:4]

        if self.request.user.is_authenticated:
            context['user_review'] = Review.objects.filter(
                product=product,
                user=self.request.user
            ).first()

        context['form'] = self.get_form()
        context['reviews'] = product.reviews.all()
        return context


class HomeView(TemplateView):
    template_name = 'core/home.html'


class ProductStockOutListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = StockOut
    template_name = 'core/product_stockout_list.html'
    context_object_name = 'stockouts'

    def test_func(self):
        return self.request.user.is_superuser  # ou is_staff, se preferir

    def handle_no_permission(self):
        raise PermissionDenied  # exibe erro 403

    def get_queryset(self):
        product_id = self.kwargs['pk']
        return StockOut.objects.filter(
            stock__product__id=product_id
        ).select_related('user', 'stock').order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(pk=self.kwargs['pk'])
        return context


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'core/review_edit.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_success_url(self):
        return self.object.product.get_absolute_url()


class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'core/brand_form.html'
    success_url = reverse_lazy('core:product_list')
