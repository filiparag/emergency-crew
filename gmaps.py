#! /bin/env python3

import googlemaps
from datetime import datetime
import time

gmaps = googlemaps.Client(key='AIzaSyAzv9r0WQeb1xFYH4eMs-96F2zvvEk5Acc')

def trajanje_voznje(origin, destination):
    commute = {
        'origin': origin,
        'destination': destination,
        'mode': 'driving',
        'traffic_model': 'pessimistic',
        'departure_time': time.time(),
        'units': 'metric',
        'waypoints': [],
        'optimize_waypoints': True,
        'alternatives': False,
        'region': 'RS'
    }
    ttime = gmaps.directions(**commute)[0]['legs'][0]['duration']['value'] / 60
    tdist = gmaps.directions(**commute)[0]['legs'][0]['distance']['value'] / 1000
    
    return [ttime, tdist]