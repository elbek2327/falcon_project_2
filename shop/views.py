from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product, Images, Customers

from shop.forms import CustomersModelForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.

class IndexView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'page_obj'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


def product_details_html(request):
    return render(request, 'shop/product-details.html')


# class based view
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product-details.html'
    context_object_name = 'product'





def product_list_html(request):
    return render(request, 'shop/product-list.html')


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product-list.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        self.category = get_object_or_404(Category, id=category_id)
        return Product.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context



class ProductImagesView(DetailView):
    model = Product
    template_name = 'shop/product-list.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Images.objects.filter(product=self.object)
        context['products'] = Product.objects.all()
        return context



class ECustomersView(ListView):
    model = Customers
    template_name = 'shop/customers.html'
    context_object_name = 'customers'




class CustomersDetailView(DetailView):
    model = Customers
    template_name = 'shop/customer_details.html'
    context_object_name = 'customer'




class CustomerCreateView(CreateView):
    model = Customers
    form_class = CustomersModelForm
    template_name = 'shop/customer_create.html'
    success_url = reverse_lazy('shop:e_customers')




class CustomerUpdateView(UpdateView):
    model = Customers
    form_class = CustomersModelForm
    template_name = 'shop/customer_update.html'
    success_url = reverse_lazy('shop:e_customers')

class CustomerDeleteView(DeleteView):
    model = Customers
    template_name = 'shop/customers.html'
    success_url = reverse_lazy('shop:e_customers')

