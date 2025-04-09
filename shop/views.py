import csv
import json
import pandas as pd
# import django_excel as excel #pip install django-excel Not used
# from textwrap import indent
from pandas.io.formats.style import Styler
from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product, Images, Customers
from django.http import HttpResponse
from shop.forms import CustomersModelForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone

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


def export_data(request):
    try:
        format = request.GET.get('format')
        if format == 'csv':
            meta = Customers._meta
            field_names = [field.name for field in meta.fields]
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="customers.csv"'
            writer = csv.writer(response)
            writer.writerow(field_names)
            for obj in Customers.objects.all():
                row = writer.writerow([getattr(obj,field) for field in field_names])
            return response
        elif format == 'json':
            response = HttpResponse(content_type='application/json')
            data = list(Customers.objects.all().values('id', 'name', 'email', 'phone_number',
                                                       'address', 'created_at', 'vat_number'))
            response.write(json.dumps(data, indent=4, default=str))
            response['Content-Disposition'] = 'attachment; filename="customers.json"'
            return response
        elif format == 'xlsx':
            try:
                customers = Customers.objects.all().values()
                df = pd.DataFrame(list(customers))

                datetime_columns = []
                for col in df.columns:
                    if df[col].dtype == 'datetime64[ns, UTC]' or df[
                        col].dtype == '<M8[ns, UTC]':  # Adjust dtype check if needed
                        datetime_columns.append(col)

                for col in datetime_columns:
                    df[col] = df[col].apply(lambda dt: dt.tz_convert(None) if pd.notnull(dt) else None)

                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=customers.xlsx'

                # Applying basic styling
                def style_specific_cell(x):
                    color = 'background-color: yellow'
                    return [color if x.name == 'name' else '' for _ in x]

                df.style.apply(style_specific_cell, axis=1).to_excel(response, index=False, engine='openpyxl')
                return response
            except Exception as e:
                print(f"Error generating XLSX: {e}")
                return HttpResponse("Error generating Excel file.", status=500)
        else:
            return HttpResponse("Invalid format specified.", status=400)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return HttpResponse("An unexpected error occurred during data export.", status=500)


