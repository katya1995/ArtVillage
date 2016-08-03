# -*- coding: utf-8 -*-
import json
from forms import UserForm, EmailForm, UserProfileForm, ShippingDetailsForm, CartAddProductForm
from models import Art, Image, UserProfile, Orders
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import *
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.decorators.http import require_POST
from cart import Cart
from django.views.decorators.csrf import csrf_exempt
import time
from django.template import RequestContext
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django_countries import countries


searching = ""


def apply_filtering(request):
    global searching
    elem = []
    small_value = float(request.GET['small_value'])
    large_value = float(request.GET['large_value'])
    checked_cats = request.GET.getlist('checked_cats')
    checked_types = request.GET.getlist('checked_types')
    sort_type = request.GET.getlist('sort_type')
    view_type = int(request.GET['view_type'])
    searchval = request.GET.getlist('search')

    if 'search' in searchval[0]:
        elem = Art.objects.filter(
            (Q(price__range=[small_value, large_value]) &
             Q(authenticate__exact="approved") &
             Q(quantity__gte=1)) & (Q(name__icontains=searching)
                                    | Q(artist__icontains=searching) | Q(identification__icontains=searching))
        )

    else:
        searching = ""
        elem = Art.objects.filter(
            Q(price__range=[small_value, large_value]),
            Q(authenticate__exact="approved"),
            Q(quantity__gte=1)
        )

    if sort_type:
        if sort_type[0] == 'asc':
            elem = elem.order_by('price')
        if sort_type[0] == "desc":
            elem = elem.order_by('-price')

    if checked_cats:
        for x in range(0, len(checked_cats)):
            s = checked_cats[x]
            s.encode('ascii', 'ignore')
            s = s.replace("_", " ")
            checked_cats[x] = s

        elem = elem.filter(
            Q(category__in=checked_cats)
        )

    if checked_types:
        for x in range(0, len(checked_types)):
            s = checked_types[x]
            s.encode('ascii', 'ignore')
            s = s.replace("_", " ")
            checked_types[x] = s

        elem = elem.filter(
            Q(sub_category__in=checked_types)
        )

    paginator = Paginator(elem, view_type)
    page = request.GET.get('page')
    try:
        art = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        art = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        art = paginator.page(paginator.num_pages)
    return render(request, 'ArtVillage/filtering.html', {'art': art, 'val': view_type})


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Order items by name in asc order
    pieces_of_art = Art.objects.order_by('name') & Art.objects.filter(authenticate__exact="approved") \
                    & Art.objects.filter(quantity__gte=1)
    # Get number of items in the catalogue
    num_items = pieces_of_art.count()
    # Get the maximum price in the catalogue
    max = 0
    for piece in pieces_of_art:
        if piece.price > max:
            max = piece.price
    # round it to the nearest divisible by 10
    if max % 10 != 0:
        rem = 10 - (max % 10)
        max += rem

    # Get he number of items to be displayed on each page
    view_type = 8
    if request.is_ajax():
        view_type = int(request.GET['view_type'])

    # Implement the paginator
    paginator = Paginator(pieces_of_art, view_type)

    page = request.GET.get('page')
    try:
        art = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        art = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        art = paginator.page(paginator.num_pages)
    # Return a rendered response to send to the client.
    return render(request, 'ArtVillage/index.html', {'art': art, 'max': max, 'num_items': num_items})


def piece_of_art(request, art_name_slug, id):
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        art = Art.objects.get(slug=art_name_slug, id=id)
        images = Image.objects.filter(name__icontains=art.identification)
        # Adds our results list to the template context under name pages.
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.

        cart_product_form = CartAddProductForm(total_quantity=art.quantity, update=False, current_quantity=1)
    except Art.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'ArtVillage/art.html',
                  {'art': art, 'cart_product_form': cart_product_form, 'images': images})


def track_art(request):
    # get the url for each piece of art
    art_id = None
    url = ''
    if request.method == 'GET':
        if 'art_id' in request.GET:
            art_id = request.GET['art_id']
            try:
                piece_art = Art.objects.get(id=art_id)
                url = '/art/{}/{}/'.format(piece_art.slug, art_id)
            except:
                pass
    return redirect(url)


def register(request):
    # Register users in the system
    context = RequestContext(request)
    email_in_db = False
    registered = False
    username_taken = False
    if request.method == 'POST':
        user_data = request.POST
        user_data['username'] = user_data['username'].strip()
        user_form = UserForm(user_data)
        profile_form = UserProfileForm(user_data)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            # c heck if email is in the database
            email_to_be_checked = user.email
            # if no user has this email, the query will result in an error, then
            # the except statement will be executed, resulting in a successful registration
            try:
                test_user = User.objects.get(email=email_to_be_checked)
                email_in_db = True
            except User.DoesNotExist:
                # save user and user_profile, and sign in the user with the non-hashed password
                non_hashed_password = user.password
                user.set_password(non_hashed_password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                registered = True
                # In the end, log the user into the system
                user2 = authenticate(username=user.username, password=non_hashed_password)
                login(request, user2)
        else:
            # convert the errors into a json format
            user_form_errors = json.loads(user_form.errors.as_json())
            # check if the user_form error was raised because someone tried to register with a username that is already in the dbs
            if user_form_errors.has_key("username") and \
                            user_form_errors['username'][0]['message'] == "User with this Username already exists.":
                username_taken = True
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render_to_response('ArtVillage/register.html', {'user_form': user_form, 'registered': registered,
                                                           'email_in_db': email_in_db, 'username_taken': username_taken,
                                                           'profile_form': profile_form}, context)


def user_login(request):
    # Login users to the system
    name = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = username
        user = authenticate(username=username, password=password)
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index/')
            return HttpResponse("Your ArtVillage account is disabled.")
        return render(request, 'ArtVillage/login.html', {"invalid": True, "name": name})
    else:
        return render(request, 'ArtVillage/login.html', {"name": name})


@login_required()
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect('/index/')


@login_required()
def profile(request, user):
    context_dict = {}
    try:
        user_can_edit = False
        userp = User.objects.get(username=user)
        try:
            up = UserProfile.objects.get(user=userp)
        except:
            up = None

        context_dict['user'] = userp
        context_dict['userprofile'] = up

        if userp == User.objects.get(username=request.user):
            user_can_edit = True
        context_dict['user_can_edit'] = user_can_edit
    except User.DoesNotExist:
        pass
    return render(request, 'ArtVillage/profile.html', context_dict)


@login_required()
def edit_details(request):
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        email = request.POST['email']
        try:
            existent_email = User.objects.get(email=email)
        except:
            existent_email = None

        if existent_email:
            return render(request, 'ArtVillage/edit_details.html', {"existent": True})

        form = EmailForm(data=request.POST, instance=request.user)
        try:
            up = UserProfile.objects.get(user=request.user)
        except:
            up = None
        if form.is_valid():
            if email:
                user = form.save(commit=False)
                user.save()
            return HttpResponseRedirect('/profile/' + user.username)
        else:
            return render(request, 'ArtVillage/edit_details.html', {})
    else:
        return render(request, 'ArtVillage/edit_details.html', {})





@login_required()
def edit_shipping_details(request):
    c = dict(countries)

    country = sorted(c.values())

    country_code = []
    for name in country:
        country_code += [(name, c.keys()[c.values().index(name)])]


    user = User.objects.get(username=request.user)
    if request.method == "POST":
        form = ShippingDetailsForm(data=request.POST, instance=UserProfile.objects.get(user=request.user))
        try:
            up = UserProfile.objects.get(user=request.user)
        except:
            up = None
        if form.is_valid():
            user_profile_obj = form.save(commit=False)
            user_profile_obj.user = request.user
            user_profile_obj.save()
            return HttpResponseRedirect('/profile/' + request.user.username)
        else:
            return render(request, 'ArtVillage/edit_shipping_details.html', {'profile_form': form, 'country': country_code})
    else:
        form = ShippingDetailsForm()
    return render(request, 'ArtVillage/edit_shipping_details.html', {'profile_form': form, 'country': country_code})


@login_required()
def change_password(request):
    form = PasswordReset(user=request.user)

    if request.method == 'POST':
        form = forms.PasswordReset(request.user, request.POST)
        if form.is_valid():
            the_form = form.save(commit=False)
            update_session_auth_hash(request, form.user)
        else:
            return render(request, 'ArtVillage/changepassword.html', {
                'form': form,
                'error': True
            })
    return render(request, 'ArtVillage/changepassword.html', {
        'form': form,
    })


def search(request):
    global searching

    if request.method == "POST":
        s = request.POST.get('search', None)
    else:
        s = ''
    searchText = str(s)
    searching = searchText
    pieces_of_art = (Art.objects.filter(name__icontains=searchText) \
                     | Art.objects.filter(artist__icontains=searchText) \
                     | Art.objects.filter(identification__icontains=searchText)) \
                    & Art.objects.filter(authenticate__exact="approved") & Art.objects.filter(quantity__gte=1)

    num_items = pieces_of_art.count()

    max = 0

    for piece in pieces_of_art:
        if piece.price > max:
            max = piece.price
    if max % 10 != 0:
        rem = 10 - (max % 10)
        max += rem

    view_type = 8
    if request.is_ajax():
        view_type = int(request.GET['view_type'])

    paginator = Paginator(pieces_of_art, view_type)

    page = request.GET.get('page')

    try:
        art = paginator.page(page)
    except PageNotAnInteger:
        art = paginator.page(1)
    except EmptyPage:
        art = paginator.page(paginator.num_pages)

    return render(request, 'ArtVillage/index.html', {'art': art, 'max': max, 'num_items': num_items})


def get_art_list(max_results=0, starts_with=''):
    art_list = []
    if starts_with:
        art_list = (Art.objects.filter(name__istartswith=starts_with) | Art.objects.filter(
            artist__icontains=starts_with) | Art.objects.filter(identification__istartswith=starts_with)) \
                   & Art.objects.filter(authenticate__exact="approved") & Art.objects.filter(quantity__gte=1)
    if max_results > 0:
        if len(art_list) > max_results:
            art_list = art_list[:max_results]
    return art_list


def suggest_art(request):
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    art_list = get_art_list(8, starts_with)
    return render(request, 'ArtVillage/suggest_art.html', {'art': art_list})


def get_new_page(request):
    if request.is_ajax():
        global searching
        small_value = float(request.GET['small_value'])
        large_value = float(request.GET['large_value'])
        checked_cats = request.GET.getlist('checked_cats')
        checked_types = request.GET.getlist('checked_types')
        sort_type = request.GET.getlist('sort_type')
        new_page = request.GET['new_page']
        view_type = int(request.GET['view_type'])
        searchval = request.GET.getlist('search')

        if 'search' in searchval[0]:
            elem = Art.objects.filter(
                (Q(price__range=[small_value, large_value]) &
                 Q(authenticate__exact="approved") &
                 Q(quantity__gte=1)) & (Q(name__icontains=searching)
                                        | Q(artist__icontains=searching) | Q(identification__icontains=searching))
            )

        else:
            searching = ""
            elem = Art.objects.filter(
                Q(price__range=[small_value, large_value]),
                Q(authenticate__exact="approved"),
                Q(quantity__gte=1)
            )

        if sort_type:
            if sort_type[0] == 'asc':
                elem = elem.order_by('price')
            if sort_type[0] == "desc":
                elem = elem.order_by('-price')

        if checked_cats:
            elem = elem.filter(
                Q(category__in=checked_cats)
            )

        if checked_types:
            elem = elem.filter(
                Q(type__in=checked_types)
            )

        paginator = Paginator(elem, view_type)
        try:
            art = paginator.page(new_page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page
            art = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            art = paginator.page(paginator.num_pages)

        return render(request, 'ArtVillage/filtering.html', {'art': art, 'val': view_type})


@require_POST
@login_required()
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Art, id=product_id)
    update = request.POST['update'] in ['True']
    quantity = int(request.POST['quantity'])
    cart.add(product=product,
             quantity=quantity,
             update_quantity=update)
    return redirect('cart_detail')


@login_required()
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Art, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


@login_required()
def cart_detail(request):
    if request.method == 'GET':
        # Get the shopping cart
        cart = Cart(request)
        print cart

        # Get delivery type (home or store)
        delivery_type = "store"
        if request.is_ajax():
            delivery_type = request.POST['delivery_type']

        # Load the user profile attributes
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except:
            userprofile = None


        # Find the largest postage price and set it as delivery price
        total_delivery_price = 0

        # Iterate over all of the items in the cart
        for item in cart:

            # If the item is out of stock, remove it
            if item['product'].quantity == 0:
                cart_remove(request, item['product'].id)
            else:
                if item['product'].postage_price > total_delivery_price:
                    total_delivery_price = item['product'].postage_price
                item['update_quantity_form'] = CartAddProductForm(
                    update=True,
                    current_quantity=item['quantity'],
                    total_quantity=item['product'].quantity
                )
        print delivery_type
        print total_delivery_price
        if delivery_type == "store":
            total_delivery_price = 0
        print total_delivery_price
        return render(request, 'ArtVillage/detail.html',
                      {'cart': cart, 'total_delivery_price': total_delivery_price, 'total_with_delivery':
                          cart.get_total_price() + total_delivery_price, 'delivery_type': delivery_type, 'userprofile': userprofile})
    else:
        # Get the shopping cart
        cart = Cart(request)
        print cart

        # Get delivery type (home or store)
        delivery_type = "store"
        if request.is_ajax():
            delivery_type = request.POST['delivery_type']

        # Load the user profile attributes
        try:
            userprofile = UserProfile.objects.get(user=request.user)
        except:
            userprofile = None


        # Find the largest postage price and set it as delivery price
        total_delivery_price = 0

        # Iterate over all of the items in the cart
        for item in cart:

            # If the item is out of stock, remove it
            if item['product'].quantity == 0:
                cart_remove(request, item['product'].id)
            else:
                if item['product'].postage_price > total_delivery_price:
                    total_delivery_price = item['product'].postage_price
                item['update_quantity_form'] = CartAddProductForm(
                    update=True,
                    current_quantity=item['quantity'],
                    total_quantity=item['product'].quantity
                )
        print delivery_type
        print total_delivery_price
        if delivery_type == "store":
            total_delivery_price = 0
        print total_delivery_price
        return render(request, 'ArtVillage/shopping_cart_table.html',
                      {'cart': cart, 'total_delivery_price': total_delivery_price, 'total_with_delivery':
                          cart.get_total_price() + total_delivery_price, 'delivery_type': delivery_type, 'userprofile': userprofile})


def about(request):
    return render(request, 'ArtVillage/about.html', None)


def cancel(request):
    return render(request, 'ArtVillage/cancel.html', None)


@csrf_exempt
def success(request):
    cart = Cart(request)
    context_dict = {}
    try:
        print ("Success view")
        print request.POST
        print ("------------")
        arg = ''
        request.parameter_storage_class = context_dict
        print ("CONTEXT DICT -----------")
        print context_dict
        values = request.POST
        print "VALUES"
        print values
        for x, y in values.iteritems():
            arg += "&{x}={y}".format(x=x, y=y)

        validate_url = 'https://www.sandbox.paypal.com' \
                       '/cgi-bin/webscr?cmd=_notify-validate{arg}' \
            .format(arg=arg)

        print "VALIDATE_URL"
        print validate_url
        r = requests.get(url=validate_url)
        print("is the request made  ")
        print(r)
        print(r.content)
        if r.text == 'VERIFIED':
            try:
                print "IT's verified"
                payer_email = request.POST['payer_email']
                unix = int(time.time())
                payment_date = request.POST['payment_date']
                username = request.POST['custom']
                last_name = request.POST['last_name']
                payment_gross = request.POST['payment_gross']
                payment_fee = request.POST['payment_fee']
                payment_net = float(payment_gross) - float(payment_fee)
                payment_status = request.POST['payment_status']
            except Exception as e:
                with open('/tmp/ipnout.txt', 'a') as f:
                    data = 'ERROR WITH IPN DATA\n' + str(values) + '\n'
                    f.write(data)

            with open('/tmp/ipnout.txt', 'a') as f:
                data = 'SUCCESS\n' + str(values) + '\n'
                f.write(data)

            user = request.user
            user.Orders.buyer = username
            user.Orders.time = unix
            user.Orders.payment_date = payment_date
            user.Orders.payment_gross = payment_gross
            user.Orders.payment_fee = payment_fee
            user.Orders.payment_net = payment_net
            if payment_status == "confirmed":
                user.Orders.payment_status = True

        else:
            with open('/tmp/ipnout.txt', 'a') as f:
                data = 'FAILURE\n' + str(values) + '\n'
                f.write(data)
    except Exception as e:
        return str(e)
    return render(request, 'ArtVillage/success.html', None)

def ipn(request):
    print "IPN View"
    print request.POST
    print "------------"
    return request.POST