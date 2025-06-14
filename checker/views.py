from django.shortcuts import render
from . import koleo_api
from datetime import date, datetime

def search_page(request):
    initial_data = {
        'start_station': '',
        'end_station': '',
        'date': date.today().strftime("%Y-%m-%d"),
        'time': datetime.now().strftime("%H:%M"),
    }

    if request.user.is_authenticated:
        initial_data['start_station'] = request.user.userprofile.default_start_station
        initial_data['end_station'] = request.user.userprofile.default_end_station

    if request.method == "POST":
        start_station = request.POST.get("start_station")
        end_station = request.POST.get("end_station")
        search_date = request.POST.get("date")
        search_time = request.POST.get("time")

        allowed_compartment_ids = [10]
        if request.user.is_authenticated:
            allowed_compartment_ids = list(
                request.user.userprofile.allowed_compartments.values_list('koleo_id', flat=True)
            )

        connections = koleo_api.find_connections(
            start_station, end_station, search_date, search_time, allowed_compartment_ids
        )

        context = {
            "connections": connections,
            "search_params": {
                "start": start_station, "end": end_station,
                "date": search_date, "time": search_time,
            },
        }
        return render(request, "checker/results.html", context)

    return render(request, "checker/search.html", {'initial': initial_data})