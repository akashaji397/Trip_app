
from django.contrib import messages
from .serializers import TripSerializers
from .models import Trip
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .forms import TripForm
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.shortcuts import render, redirect
import requests


class TripCreateView(generics.ListCreateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializers  # Corrected this line
    permission_classes = [AllowAny]

class TripDetail(generics.RetrieveAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializers  # Corrected this line

class TripUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializers  # Corrected this line

class TripDelete(generics.DestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializers  # Corrected this line


class TripSearchViewset(generics.ListAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializers

    def get_queryset(self):
        place_name = self.kwargs.get('place_name')
        return Trip.objects.filter(place_name__icontains=place_name)




def create_trip(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                trip = form.save()  # Save the form and get the instance
                api_url = 'http://127.0.0.1:8001/create/'  # Ensure this URL is correct
                data = {
                    'place_name': trip.place_name,
                    'weather': trip.weather,
                    'state': trip.state,
                    'district': trip.district,
                    'google_map_link': trip.google_map_link,
                    'description': trip.description,
                }
                files = {
                    'Trip_img': request.FILES.get('Trip_img')
                }

                print(data)  # For debugging purposes

                # Send data and file via POST request
                response = requests.post(api_url, data=data, files=files)
                
                # Check for success or error
                if response.status_code == 200:
                    messages.success(request, 'Data inserted successfully')
                    return redirect('index')  # Redirect to the index page
                else:  
                    messages.error(request, f'Error {response.status_code}: {response.text}')
                    return redirect('index') 

            except requests.RequestException as e:  # Corrected exception class
                messages.error(request, f'Error during API request: {str(e)}')
        else:
            messages.error(request, 'Form is invalid. Please check the entered data.')
    else:
        form = TripForm()  # Corrected form initialization
    return render(request, 'create_trip.html', {'form': form})




def index(request):
    if request.method == 'POST':
        search = request.POST.get('search', '').strip()
        api_url = f'http://127.0.0.1:8001/search/{search}/'

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
            else:
                data = None
        
        except requests.RequestException as e:
            data = None

        return render(request, 'index.html', {'data': data})

    else:
        api_url = f'http://127.0.0.1:8001/create/'

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                data = response.json()
                original_data = data

                paginator = Paginator(original_data, 6)

                try:
                    page = int(request.GET.get('page', 1))
                except (ValueError, TypeError):
                    page = 1

                try:
                    trips = paginator.page(page)
                except (EmptyPage, InvalidPage):
                    trips = paginator.page(paginator.num_pages)

                context = {
                    'original_data': original_data,
                    'trips': trips,
                }

                return render(request, 'index.html', context=context)
            else:
                return render(request, 'index.html', {'error_message': f'Error: {response.status_code}'})
        
        except requests.RequestException as e:
            return render(request, 'index.html', {'error_message': f'Error: {str(e)}'})


def update_detail(request, id):
    api_url = f'http://127.0.0.1:8001/detail/{id}/'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
    return render(request, 'trip_update.html', {'trips': data})

def update_trip(request, id):
    if request.method == "POST":
        place_name = request.POST.get('place_name', '')
        weather = request.POST.get('weather', '')
        state = request.POST.get('state', '')
        district = request.POST.get('district', '')
        google_map_link = request.POST.get('google_map_link', '')
        description = request.POST.get('description', '')
        
        api_url = f'http://127.0.0.1:8001/update/{id}/'

        data = {
            'place_name':place_name,
            'weather':weather,
            'state': state,
            'district':district,
            'google_map_link':google_map_link,
            'description':description,
            }
        files = {
                'Trip_img': request.FILES.get('Trip_img')
            }

        response = requests.put(api_url, data=data, files=files)

        print('Response:', response.text)  # Log the response for debugging

        if response.status_code == 200:
            messages.success(request, 'Recipe updated successfully')
            return redirect('index')
        else:
            messages.error(request, f'Error submitting data to the REST API: {response.status_code}')
            return redirect('index')
    return render(request, 'trip_update.html')



def trip_fetch(request,id):
    api_url= f'http://127.0.0.1:8001/detail/{id}/'
    response = requests.get(api_url)
    if response.status_code==200:
        data=response.json()
        return render(request,'trip_fetch.html',{'trips': data})
    return render(request,'trip_fetch.html')



def trip_delete(request,id):
    api_url= f'http://127.0.0.1:8000/delete/{id}/'
    response=requests.delete(api_url)
    if response.status_code==200:
        print(f'Item with id {id} has been deleted')
    else:
        print(f'Failed to delete item. status_code {response.status_code}')
    return redirect('/')



def trip_search(request):
    query = request.GET.get('name', '').strip()  # Retrieve the search term
    results = []

    if query:
        
        # Directly query the database using Django ORM
        results = Trip.objects.filter(place_name__icontains=query)
        
        if not results.exists():
            messages.info(request, f'No recipes found for "{query}".')
    else:
        messages.info(request, 'Please enter a search term.')

    return render(request, 'search_results.html', {'results': results, 'query': query})