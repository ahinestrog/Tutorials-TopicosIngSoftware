from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect 
from django.views.generic import TemplateView 
from django.views import View
from django import forms

# Create your views here.
#def homePageView(request):
    # return HttpResponse('Hello, World!')
    #return render(request, 'pages/home.html')

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About Us - Online Store",
            "subtitle": "About Us",
            "description": "This is an about page...",
            "author": "Develop by: Alejandro"
        })

        return context
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact Us - Online Store",
            "subtitle": "Contact Us",
            "description": "This is a contact page...",
            "author": "Develop by: Alejandro",
            "email": "info@example.com",
            "address": "123 Main St, City, State, 12345",
            "phone": "555-555-5555",
        })

        return context

class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 1000},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 1500},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 2000},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 500},
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        try:
            product = Product.products[int(id) - 1]
        except (IndexError, ValueError):  # Para cuando el indice no es valido
            return HttpResponseRedirect('/')  # Lo redirige al home

        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Agregue un precio mayor a 0")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'
    
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            return redirect('product_created')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            return render(request, self.template_name, viewData)

class ProductCreatedView(TemplateView):
        template_name = 'products/product_created.html'
