from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import format_html
from .serializers import ProductSerializer
import csv
import folium
from folium.plugins import FastMarkerCluster
from folium.plugins import MarkerCluster

from search.models import Address, Cpa, Customer, Product, Tuning


# Create your views here.
def models_api(request):
    brand = request.GET.get('brand')
    models = list(Product.objects.filter(brand=brand))
    serializer = ProductSerializer(models, many=True)
    data = serializer.data
    options = []
    for model in models:
        option = f'<option value="{model.pid}">{model.model}</option>'
        options.append(option)
    response_data = {'models': data, 'options': options}
    
    return JsonResponse(response_data, safe=False)

def SearchFilterView(request):
    # for name search
    customers = Customer.objects.all()

    # for email
    emails = Customer.objects.values_list('email', flat=True)
    emails = list(map(str, emails))

    # for address search
    addresses = Address.objects.all()

    # for product search
    products = Product.objects.values_list('brand', flat=True).distinct()
    products = list(map(str, products))

    # for model
    models = Product.objects.all()

    if request.method == 'GET':

        autocomplete_name_query = request.GET.get('customer_name_auto')
        autocomplete_email_query = request.GET.get('customer_email')
        autocomplete_address_query = request.GET.get('auto_address')
        customer_phone_query = request.GET.get('customer_phone')
        autocomplete_product_query = request.GET.get('product_brand')
        product_type_query = request.GET.get('product_type')
        product_model_query = request.GET.get('product_submodel')
        tuning_date_query = request.GET.get('tuning_date')

        search_result = []

        customers_name = []
        customers_email = []
        customers_address_auto = []
        customers_phone = []
        customers_product = []
        customers_product_type = []
        customers_product_brand_and_type = []
        customers_product_model = []
        customers_product_brand_and_model = []
        customers_tuning = []
       

        # search from customer name
        if autocomplete_name_query != '' and autocomplete_name_query is not None:
            # your raw SQL query
            raw_query = "select cpa.cid, customer.firstname, customer.lastname, customer.email, customer.phone, address.address, address.suburb, address.postcode, product.brand, product.model, product.type, address.latitude, address.longitude, address.aid from cpa cross join customer on cpa.cid = customer.cid cross join address on cpa.aid = address.aid cross join product on cpa.pid = product.pid WHERE concat_ws(' ',customer.firstname,customer.lastname) LIKE %s"
            # execute the raw SQL query
            with connection.cursor() as cursor:
                cursor.execute(raw_query, [f'%{autocomplete_name_query}%'])
                results = cursor.fetchall()

            # create a list of dictionaries to store the results
            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': row[11], 
                    'longitude': row[12],
                    'aid': row[13]
                }
                customers_name.append(customer)
            search_result.append(autocomplete_name_query)
        # search from customer email
        if autocomplete_email_query != '' and autocomplete_email_query is not None:
            # your raw SQL query
            raw_query = "select cpa.cid, customer.firstname, customer.lastname, customer.email, customer.phone, address.address, address.suburb, address.postcode, product.brand, product.model, product.type, address.latitude, address.longitude, address.aid from cpa cross join customer on cpa.cid = customer.cid cross join address on cpa.aid = address.aid cross join product on cpa.pid = product.pid WHERE customer.email = %s"
            # execute the raw SQL query
            with connection.cursor() as cursor:
                cursor.execute(raw_query, [autocomplete_email_query])
                results = cursor.fetchall()

            # create a list of dictionaries to store the results
            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': row[11], 
                    'longitude': row[12],
                    'aid': row[13]
                }
                customers_email.append(customer)
            search_result.append(autocomplete_email_query)
        # search from customer address,suburb,postcode
        if autocomplete_address_query != '' and autocomplete_address_query is not None:
            # your raw SQL query
            raw_query = "select cpa.cid, customer.firstname, customer.lastname, customer.email, customer.phone, address.address, address.suburb, address.postcode, product.brand, product.model, product.type, address.latitude, address.longitude, address.aid from cpa cross join customer on cpa.cid = customer.cid cross join address on cpa.aid = address.aid cross join product on cpa.pid = product.pid WHERE concat_ws(' ',address.address,address.suburb,address.postcode) LIKE %s ORDER BY cpa.cid ASC"
            # execute the raw SQL query
            with connection.cursor() as cursor:
                cursor.execute(raw_query, [f'%{autocomplete_address_query}%'])
                results = cursor.fetchall()

            # create a list of dictionaries to store the results
            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': row[11], 
                    'longitude': row[12],
                    'aid': row[13]
                }
                customers_address_auto.append(customer)
            search_result.append(autocomplete_address_query)
        # search from customer phone for exact match
        if customer_phone_query != '' and customer_phone_query is not None:
            raw_query = "select cpa.cid, customer.firstname, customer.lastname, customer.email, customer.phone, address.address, address.suburb, address.postcode, product.brand, product.model, product.type, address.latitude, address.longitude, address.aid from cpa cross join customer on cpa.cid = customer.cid cross join address on cpa.aid = address.aid cross join product on cpa.pid = product.pid WHERE customer.phone = %s"

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [customer_phone_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': row[11], 
                    'longitude': row[12],
                    'aid': row[13]
                }
                customers_phone.append(customer)
            search_result.append(customer_phone_query)
        # search from piano brand
        if autocomplete_product_query != '' and autocomplete_product_query is not None and product_type_query == '0' and product_model_query == '0':
            raw_query = "select cpa.cid, customer.firstname, customer.lastname, customer.email, customer.phone, address.address, address.suburb, address.postcode, product.brand, product.model, product.type, address.latitude, address.longitude, address.aid from cpa cross join customer on cpa.cid = customer.cid cross join address on cpa.aid = address.aid cross join product on cpa.pid = product.pid WHERE product.brand = %s" 

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [autocomplete_product_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': row[11], 
                    'longitude': row[12],
                    'aid': row[13]
                }
                customers_product.append(customer)
            search_result.append(autocomplete_product_query)
        # search from piano type
        if product_type_query != '0' and autocomplete_product_query == '' or autocomplete_product_query is None :
            raw_query = "select cpa.cid, customer.firstname, customer.lastname, customer.email, customer.phone, address.address, address.suburb, address.postcode, product.brand, product.model, product.type, address.latitude, address.longitude, address.aid from cpa cross join customer on cpa.cid = customer.cid cross join address on cpa.aid = address.aid cross join product on cpa.pid = product.pid WHERE product.type = %s"

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [product_type_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': row[11], 
                    'longitude': row[12],
                    'aid': row[13]
                }
                customers_product_type.append(customer)
            search_result.append(product_type_query)
        # search from piano model
        if product_model_query != '' and product_model_query != '0' and autocomplete_product_query == '':
            raw_query = "select cpa.cid, customer.firstname, customer.lastname, customer.email, customer.phone, address.address, address.suburb, address.postcode, product.brand, product.model, product.type, address.latitude, address.longitude, address.aid from cpa cross join customer on cpa.cid = customer.cid cross join address on cpa.aid = address.aid cross join product on cpa.pid = product.pid WHERE product.pid =%s"

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [product_model_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': row[11], 
                    'longitude': row[12],
                    'aid': row[13]
                }
                customers_product_model.append(customer)
            search_result.append(f'product ID: {product_model_query}')
        # search from piano brand and model
        if autocomplete_product_query != '' and product_model_query != '0':
            raw_query = "select cpa.cid, customer.firstname, customer.lastname, customer.email, customer.phone, address.address, address.suburb, address.postcode, product.brand, product.model, product.type, address.latitude, address.longitude, address.aid from cpa cross join customer on cpa.cid = customer.cid cross join address on cpa.aid = address.aid cross join product on cpa.pid = product.pid WHERE product.brand =%s and product.pid =%s"

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [autocomplete_product_query,product_model_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': row[11], 
                    'longitude': row[12],
                    'aid': row[13]
                }
                customers_product_brand_and_model.append(customer)
            search_result.append(f'{autocomplete_product_query,product_model_query}')
        # search from piano and type
        if autocomplete_product_query != '' and product_type_query != '0':
            raw_query = "select cpa.cid, customer.firstname, customer.lastname, customer.email, customer.phone, address.address, address.suburb, address.postcode, product.brand, product.model, product.type, address.latitude, address.longitude, address.aid from cpa cross join customer on cpa.cid = customer.cid cross join address on cpa.aid = address.aid cross join product on cpa.pid = product.pid WHERE product.brand =%s and product.type = %s"

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [autocomplete_product_query,product_type_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': row[11], 
                    'longitude': row[12],
                    'aid': row[13]
                }
                customers_product_brand_and_type.append(customer)
            search_result.append(f'{autocomplete_product_query,product_type_query}')

        # search from last tuning date
        if tuning_date_query != '0' and tuning_date_query != '':
            raw_query = "select cpa.cid, customer.firstname, customer.lastname, customer.email, customer.phone, address.address, address.suburb, address.postcode, product.brand, product.model, product.type, address.latitude, address.longitude, address.aid from cpa cross join customer on cpa.cid = customer.cid cross join address on cpa.aid = address.aid cross join product on cpa.pid = product.pid cross join tuning on cpa.cid = tuning.cid WHERE tuning.tuning_date < DATE_SUB(NOW(), INTERVAL %s MONTH)"

            with connection.cursor() as cursor:
                cursor.execute(raw_query, [tuning_date_query])
                results = cursor.fetchall()

            for row in results:
                customer = {
                    'id': row[0],
                    'first_name': row[1],
                    'last_name': row[2],
                    'email': row[3],
                    'phone': row[4],
                    'address': row[5],
                    'suburb': row[6],
                    'postcode': row[7],
                    'brand': row[8],
                    'model': row[9],
                    'type': row[10],
                    'latitude': row[11], 
                    'longitude': row[12],
                    'aid': row[13]
                }
                customers_tuning.append(customer)
            search_result.append(tuning_date_query)

        # combine lists
        unique_result = customers_phone + customers_address_auto + customers_product + customers_name + customers_email + customers_product_type + customers_product_brand_and_type + customers_product_model + customers_product_brand_and_model + customers_tuning
        # remove duplicates
        unique_result = [dict(t) for t in {tuple(d.items()) for d in unique_result}]
        # retrieve search result from session
        request.session['search_result'] = unique_result

        # map visualization
        customer_house = request.session.get('search_result', [])
        if customer_house =='':
            # set customer_house to 1 if no search result for map remain on the page
            customer_house = 1
        else:
            # create Folium map randomly centered 
            mapdisplay = folium.Map(location=[-37.8136, 144.9631], zoom_start=10)
            marker_cluster = MarkerCluster()
            # latitude_map = []
            # longitude_map = []

            # add markers for all houses
            for house in customer_house:
                house_id = house['aid']
                location = list(Address.objects.filter(aid=house_id))
                
                for address in location:
                    latitude = address.latitude
                    longitude = address.longitude
                    address = location[0].address
                    suburb = location[0].suburb
                    postcode = location[0].postcode

                    # latitude_map.append(latitude)
                    # longitude_map.append(longitude)
                    
                    # format the address as a string with a tooltip prefix
                    tooltip_text = "Address: {} {} {}".format(address, suburb, postcode)

                    # single marker
                    coordinates = (latitude, longitude)
                    folium.Marker(coordinates, popup=tooltip_text).add_to(mapdisplay)
                    # marker = folium.Marker(location=[latitude, longitude], popup=tooltip_text)
                    # add the marker to the MarkerCluster
                    # marker_cluster.add_child(marker)

            # add the MarkerCluster to the map
            # mapdisplay.add_child(marker_cluster)
            # convert map to html
            m = mapdisplay._repr_html_()

    return render(request, 'search.html', {'searched':search_result,'customers': unique_result,'names':customers,'emails':emails, 'addresses': addresses,'products':products,'models':models,'nbar': 'search','map_html':m})

def export_csv(request):
        # retrieve search results
        results_list = request.session.get('search_result', [])
        # create the HttpResponse object with CSV header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="search_results.csv"'

        # create a writer object for CSV
        writer = csv.writer(response)

        # write the header row
        writer.writerow(['cid', 'first_name', 'last_name', 'email', 'phone', 'address', 'suburb', 'postcode', 'brand', 'model', 'type'])

        # write the data rows
        for result in results_list:
            writer.writerow([result['id'], result['first_name'], result['last_name'], result['email'], result['phone'], result['address'], result['suburb'], result['postcode'], result['brand'], result['model'], result['type']])

        return response

# for map.html
def MapView(request):

    return render(request, 'map.html', {'nbar': 'map'})

def DashbordView(request):
    # map visualization for all customer 
    locations = Address.objects.all()
    mapdisplay = folium.Map(location=[-37.8136, 144.9631], zoom_start=10)

    latitude = [location.latitude for location in locations]
    longitude = [location.longitude for location in locations]

    FastMarkerCluster(data=list(zip(latitude, longitude))).add_to(mapdisplay)
    # convert map to html
    m = mapdisplay._repr_html_()

    return render(request, 'dashboard.html', {'nbar': 'dashboard','map_dashboard':m})
