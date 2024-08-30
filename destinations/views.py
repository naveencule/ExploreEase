from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404, redirect
from .models import Destination
from .serializers import DestinationSerializer
from .forms import DestinationForm

# API ViewSet for CRUD operations
class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

# Views for HTML rendering
def destination_list(request):
    query = request.GET.get('q')  # Get the search query from the request
    if query:
        destinations = Destination.objects.filter(place_name__icontains=query)
    else:
        destinations = Destination.objects.all()
    return render(request, 'destination_list.html', {'destinations': destinations})


def destination_detail(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    return render(request, 'destination_detail.html', {'destination': destination})

def destination_create(request):
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('destination_list')
    else:
        form = DestinationForm()
    return render(request, 'destination_form.html', {'form': form})

def destination_update(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            return redirect('destination_list')
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'destination_form.html', {'form': form})

def destination_delete(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == "POST":
        destination.delete()
        return redirect('destination_list')
    return render(request, 'destination_confirm_delete.html', {'destination': destination})

