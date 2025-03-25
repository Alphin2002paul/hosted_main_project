from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import CarListing, Subscription  # Add Subscription import
from django.core.paginator import Paginator
from .models import CertifiedCar, CertifiedCarImage, Brand
from django.db.models import Q
from django.core.paginator import Paginator
from .models import CertifiedCar, CertifiedCarImage, Brand, Manufacturer, CarModel
from django.core.exceptions import PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.contrib import messages

@login_required
def listedcar_sub(request):
    # Get all car listings for the current user
    user_listings = CarListing.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'user_listings': user_listings
    }
    return render(request, 'listedcar_sub.html', context)

def certified_cars(request):
    # Get filter parameters from request
    search_query = request.GET.get('search', '')
    brand_id = request.GET.get('brand')
    price_range = request.GET.get('price_range')
    year = request.GET.get('year')

    # Check subscription status if user is logged in
    subscription_expired = False
    subscription = None
    if request.user.is_authenticated:
        try:
            subscription = Subscription.objects.filter(
                user=request.user,
                status='completed'
            ).latest('created_at')
            
            if subscription:
                subscription_expired = not subscription.is_active()
        except Subscription.DoesNotExist:
            subscription = None

    # Base queryset for available cars only
    cars = CertifiedCar.objects.filter(car_status='Available').select_related('manufacturer', 'model_name')

    # Apply filters
    if search_query:
        cars = cars.filter(
            Q(manufacturer__company_name__icontains=search_query) |
            Q(model_name__model_name__icontains=search_query)
        )

    if brand_id:
        cars = cars.filter(manufacturer_id=brand_id)

    if price_range:
        if price_range == '5000000+':
            cars = cars.filter(price__gte=5000000)
        else:
            min_price, max_price = map(int, price_range.split('-'))
            cars = cars.filter(price__gte=min_price, price__lte=max_price)

    if year:
        cars = cars.filter(year=year)

    # Get all brands for the filter dropdown
    brands = Brand.objects.all()

    # Pagination
    paginator = Paginator(cars, 6)  # Show 6 cars per page
    page = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    # Check if there are no cars after filtering
    no_cars = not page_obj.object_list.exists()

    context = {
        'page_obj': page_obj,
        'brands': brands,
        'no_cars': no_cars,
        'subscription': subscription,
        'subscription_expired': subscription_expired
    }

    return render(request, 'certified_cars.html', context)

def certified_cars(request):
    # Get filter parameters from request
    search_query = request.GET.get('search', '')
    brand_id = request.GET.get('brand', '')
    price_range = request.GET.get('price_range', '')
    year = request.GET.get('year', '')

    # Base queryset for approved cars
    cars = CertifiedCar.objects.filter(car_status='Approved')

    # Apply filters if provided
    if search_query:
        cars = cars.filter(
            Q(manufacturer__company_name__icontains=search_query) |
            Q(model_name__model_name__icontains=search_query)
        )

    if brand_id:
        cars = cars.filter(manufacturer_id=brand_id)

    if price_range:
        if price_range == '5000000+':
            cars = cars.filter(price__gte=5000000)
        else:
            min_price, max_price = map(int, price_range.split('-'))
            cars = cars.filter(price__gte=min_price, price__lte=max_price)

    if year:
        cars = cars.filter(year=year)

    # Get all brands for the filter dropdown
    brands = Brand.objects.all()

    # Check if there are no cars after filtering
    no_cars = not cars.exists()

    # Pagination
    paginator = Paginator(cars, 6)  # Show 6 cars per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get liked cars for the current user
    liked_cars = []
    if request.user.is_authenticated:
        liked_cars = request.user.liked_cars.values_list('id', flat=True)

    context = {
        'page_obj': page_obj,
        'brands': brands,
        'no_cars': no_cars,
        'liked_cars': liked_cars,
    }

    return render(request, 'certified_cars.html', context)

@login_required
def certified_cars_view(request):
    # Get all certified cars initially
    certified_cars = CertifiedCar.objects.all().order_by('-created_at')
    
    # Get filter parameters from request
    manufacturer = request.GET.get('manufacturer')
    model = request.GET.get('model')
    price_range = request.GET.get('price_range')
    year = request.GET.get('year')
    
    # Apply filters if they exist
    if manufacturer:
        certified_cars = certified_cars.filter(manufacturer__company_name=manufacturer)
    
    if model:
        certified_cars = certified_cars.filter(model_name__model_name=model)
    
    if price_range:
        if price_range != '5000000+':
            min_price, max_price = map(int, price_range.split('-'))
            certified_cars = certified_cars.filter(price__gte=min_price, price__lte=max_price)
        else:
            certified_cars = certified_cars.filter(price__gte=5000000)
    
    if year:
        certified_cars = certified_cars.filter(year=year)
    
    # Get liked cars for the current user
    liked_cars = []
    if request.user.is_authenticated:
        liked_cars = [like.car.id for like in request.user.carlike_set.all()]
    
    # Pagination
    paginator = Paginator(certified_cars, 9)  # Show 9 cars per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all manufacturers and models for filter dropdowns
    manufacturers = Manufacturer.objects.all()
    car_models = CarModel.objects.all()
    
    context = {
        'page_obj': page_obj,
        'manufacturers': manufacturers,
        'car_models': car_models,
        'liked_cars': liked_cars,
        'no_cars': len(certified_cars) == 0,
        # Preserve filter values in context
        'selected_manufacturer': manufacturer,
        'selected_model': model,
        'selected_price_range': price_range,
        'selected_year': year,
    }
    
    return render(request, 'certified_cars.html', context)

@login_required
def certified_car_detail(request, car_id):
    try:
        certified_car = CertifiedCar.objects.get(id=car_id)
        # Check if the car is liked by the current user
        is_liked = request.user.carlike_set.filter(car=car_id).exists() if request.user.is_authenticated else False
        
        context = {
            'car': certified_car,
            'is_liked': is_liked,
        }
        return render(request, 'certified_car_detail.html', context)
    except CertifiedCar.DoesNotExist:
        return render(request, '404.html', {'message': 'Certified Car not found'})

def approved_certified_cars(request):
    # Get only approved certified cars
    certified_cars = CertifiedCar.objects.filter(car_status='Approved').order_by('-created_at')
    
    # Get the list of cars liked by the user
    liked_cars = []
    if request.user.is_authenticated:
        liked_cars = [like.car.id for like in CarLike.objects.filter(user=request.user)]
    
    # Pagination
    paginator = Paginator(certified_cars, 9)  # Show 9 cars per page
    page = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    
    context = {
        'page_obj': page_obj,
        'liked_cars': liked_cars,
        'no_cars': len(certified_cars) == 0,
    }
    
    return render(request, 'certified_cars.html', context)

@login_required
@require_POST
def approve_car_listing(request, car_id):
    try:
        data = json.loads(request.body)
        remarks = data.get('remarks')
        
        car = CertifiedCar.objects.get(id=car_id)
        car.car_status = 'Approved'
        car.admin_remarks = remarks
        car.approval_date = timezone.now()
        car.save()
        
        # Here you can add email notification logic if needed
        
        return JsonResponse({
            'success': True,
            'message': 'Car listing approved successfully'
        })
    except CertifiedCar.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Car listing not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
@require_POST
def cancel_car_listing(request, car_id):
    try:
        data = json.loads(request.body)
        reason = data.get('reason')
        
        car = CertifiedCar.objects.get(id=car_id)
        car.car_status = 'Denied'
        car.admin_remarks = reason
        car.denial_date = timezone.now()
        car.save()
        
        # Here you can add email notification logic if needed
        
        return JsonResponse({
            'success': True,
            'message': 'Car listing cancelled successfully'
        })
    except CertifiedCar.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Car listing not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def certified_car_admin_details(request, car_id):
    try:
        car = CertifiedCar.objects.get(id=car_id)
        images = CertifiedCarImage.objects.filter(certified_car=car)
        user = car.user  # Get the user who submitted the car

        context = {
            'car': car,
            'images': images,
            'user_details': {
                'name': f"{user.first_name} {user.last_name}",
                'username': user.username,
                'email': user.email,
                'phone_number': user.Phone_number,
            }
        }
        return render(request, 'salemoredetails_certified.html', context)
    except CertifiedCar.DoesNotExist:
        messages.error(request, 'Car not found.')
        return redirect('certified_admin_req')