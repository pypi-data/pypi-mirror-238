import requests
import os
import json


GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')


def call(path, args):
    args['key'] = GOOGLE_MAPS_API_KEY
    parameters = '&'.join(f'{key}={value.replace(" ", "+")}' for key, value in args.items())
    return requests.get(f'https://maps.googleapis.com/maps/api/{path}?{parameters}').json()


def get_directions(start, goal):
    response = call('directions/json', {
        'origin': start,
        'destination': goal,
        'mode': 'transit'
    })

    print(json.dumps(response, sort_keys=True, indent=4))
    trips = []
    for route in response['routes']:
        steps = []
        for step in route['legs'][0]['steps']:
            if step['travel_mode'] != 'TRANSIT':
                print(step)
                if step['distance']['value'] > 500:
                    steps.append({
                        'vehicle': 'Walking',
                        'line': '',
                        'distance': step['distance']['text'],
                        'destination': step['html_instructions']
                    })
                continue
            print(step)
            steps.append({
                'vehicle': step['transit_details']['line']['vehicle']['name'],
                'line': step['transit_details']['line']['short_name'],
                'distance': step['distance']['text'],
                'destination': step['transit_details']['arrival_stop']['name']
            })
        trips.append({
            'arrival': route['legs'][0]['arrival_time'],
            'departure': route['legs'][0]['departure_time'],
            'duration': route['legs'][0]['duration'],
            'steps': steps
        })

    print(json.dumps(trips, sort_keys=True, indent=4))
    return trips


if __name__ == '__main__':
    response = getDirections('Stenhøj Have 23', 'Rudegaard stadion, holte')
    print(response)
