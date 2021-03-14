from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from courses.models import Course
from enroll.models import Enroll
from .cart import Cart

@require_POST
def cart_add(request, slug):
    cart = Cart(request)
    course = get_object_or_404(Course, slug=slug)
    cart.add(course=course, quantity=1, update_quantity=False)
    return redirect('cart:cart_detail')

def cart_remove(request, slug):
    cart = Cart(request)
    course = get_object_or_404(Course, slug=slug)
    cart.remove(course)
    return redirect('cart:cart_detail')

def cart_detail(request):
    print("YES YEY YES")
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

def cart_checkout(request):
    carts = Cart(request)
    for cart in carts:
        course = cart['course']
        Enroll.objects.create(course=course, user_id=request.user.id)
    messages.success(request, 'Successfully checked out!')
    carts.clear()
    return redirect(reverse_lazy('cart:cart_detail'))