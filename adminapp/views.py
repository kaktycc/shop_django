from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test
import datetime
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from adminapp.forms import ShopUserCreateForm, ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm


# Create your views here.
class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/main.html'

    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UserListView, self).dispatch(*args, **kwargs)

class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_create.html'
    success_url = reverse_lazy('admin:main')
    form_class = ShopUserCreateForm

class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:main')
    form_class = ShopUserAdminEditForm

class UserDeleteView(DeleteView):
    model = ShopUser
    fields = '__all__'
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:main')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

def user_repair(request, pk):
    user_del = get_object_or_404(ShopUser, pk=int(pk))
    user_del.is_active = True
    user_del.save()
    return HttpResponseRedirect(reverse('admin:main'))

@user_passes_test(lambda user: user.is_superuser)
def categories(request):
    title = 'админка'

    category_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': category_list,
    }

    return render(request, 'adminapp/categories.html', context)

class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    success_url = reverse_lazy('admin:categories')
    fields = ('__all__')

class ProductCategoryEditView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryEditView, self).get_context_data(**kwargs)
        context['title'] = 'категории\редактирование'
        return context


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

def category_repair(request, pk):
    cat_del = get_object_or_404(ProductCategory, pk=int(pk))
    cat_del.is_active = True
    cat_del.save()
    return HttpResponseRedirect(reverse('admin:categories'))

def category_products(request, category_pk):
    title = 'продукты категории'
    cat_products = get_object_or_404(ProductCategory, pk=int(category_pk))
    # products = cat_products.product_set.all()
    products = Product.objects.filter(category=cat_products)

    context = {
        'title': title,
        'category_products': cat_products,
        'object_list': products,

    }
    return render(request, 'adminapp/products.html', context)


def product_create(request, category_pk):
    title = 'новый продукт'
    category = get_object_or_404(ProductCategory, pk=category_pk)

    if request.method == 'POST':
        product_create_form = ProductEditForm(request.POST, request.FILES)

        if product_create_form.is_valid():
            product_create_form.save()
            return HttpResponseRedirect(reverse('admin:category_products', args=[category_pk]))
    else:
        product_create_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'product_create_form': product_create_form,
        'category': category,
        'date_time': datetime.date.today,
    }
    return render(request, 'adminapp/product_create.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product.html'


def product_update(request, pk):
    title = 'редактирование продукта'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)

        if product_edit_form.is_valid():
            product_edit_form.save()
            return HttpResponseRedirect(reverse('admin:category_products', args=[edit_product.category_id]))
    else:
        product_edit_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'product_edit_form': product_edit_form,
        'category': edit_product.category,
        'date_time': datetime.date.today,
    }
    return render(request, 'adminapp/product_update.html', context)


def product_delete(request, pk):
    title = 'удаление продукта'

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin:category_products', args=[product.category.pk]))

    context = {
        'title': title,
        'product_to_delete': product,
        'date_time': datetime.date.today,
    }
    return render(request, 'adminapp/product_delete.html', context)


def product_repair(request, pk):
    product_del = get_object_or_404(Product, pk=int(pk))
    product_del.is_active = True
    product_del.save()
    return HttpResponseRedirect(reverse('admin:category_products', args=[product_del.category.pk]))
