from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Event
from .forms import EventForm


def is_admin(user):
    return user.is_superuser


# -------------------------
# Admin Event Management
# -------------------------

@login_required
@user_passes_test(is_admin)
def create_event_admin(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("events:event_list")
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form})


@login_required
@user_passes_test(is_admin)
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("events:event_list")
    else:
        form = EventForm(instance=event)
    return render(request, "events/event_form.html", {"form": form})


# -------------------------
# User Event Views
# -------------------------

def create_event(request):
    if request.method == 'POST':
        sec = int(request.POST['seconds'])
        Event.objects.create(
            name=request.POST['name'],
            event_date=timezone.now() + timedelta(seconds=sec)
        )
        return redirect('events:list')
    return render(request, 'events/create.html')


# -------------------------
# Public Views
# -------------------------

def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('event_date')
    return render(request, "events/event_list.html", {"events": events})


def event_detail(request, uid):
    event = get_object_or_404(Event, uid=uid)
    return render(request, "events/event_detail.html", {"event": event})


def api_featured_events(request):
    """API endpoint to get featured/active events for homepage with priority ordering"""
    count = int(request.GET.get('count', 4))  # Default to 4 events
    
    # Get active events and order by priority: live -> soon -> end
    from django.db.models import Case, When, IntegerField
    
    events = Event.objects.filter(is_active=True).annotate(
        priority=Case(
            When(status='live', then=1),
            When(status='soon', then=2),
            When(status='end', then=3),
            When(status='pending', then=4),
            When(status='cancelled', then=5),
            default=6,
            output_field=IntegerField()
        )
    ).order_by('priority', 'event_date')[:count]
    
    data = {
        'events': [
            {
                'id': event.id,
                'uid': str(event.uid),
                'name': event.name,
                'description': event.description[:100] if event.description else '',
                'event_type': event.get_event_type_display(),
                'discount': event.discount_percentage,
                'banner': event.banner_image.url if event.banner_image else '/static/images/event-placeholder.jpg',
                'status': event.status,
                'is_cancelled': event.status == 'cancelled',
                'is_ongoing': event.status == 'live',
                'is_upcoming': event.status == 'soon',
                'is_ended': event.status == 'end',
                'event_date': event.event_date.isoformat() if event.event_date else None,
                'countdown': str(event.countdown()) if event.countdown() else None,
            }
            for event in events
        ]
    }
    return JsonResponse(data)


def index(request):
    return HttpResponse("Events Home Page")
