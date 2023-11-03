import bz2
import csv
import os

import requests

from routing.models import SolarSystem, SolarSystemConnection, TrigInvasion


def pull_data_solarsystems():
    mapjumps_url = 'https://www.fuzzwork.co.uk/dump/latest/mapSolarSystems.csv.bz2'
    SolarSystem.objects.all().delete()

    connections = []

    with open('mapSolarSystems.csv.bz2', 'wb') as f:
        f.write(requests.get(mapjumps_url).content)

    open('mapSolarSystems.csv', 'wb').write(
        bz2.open('mapSolarSystems.csv.bz2', 'rb').read())

    with open('mapSolarSystems.csv', encoding='UTF-8') as f:
        csv_file = csv.reader(f)
        next(csv_file)  # skip headers
        for row in csv_file:
            connections.append(SolarSystem(id=row[2], security_status=row[21]))

    SolarSystem.objects.bulk_create(connections, batch_size=500, ignore_conflicts=True)


def pull_data_connections():
    mapjumps_url = 'https://www.fuzzwork.co.uk/dump/latest/mapSolarSystemJumps.csv.bz2'
    SolarSystemConnection.objects.all().delete()

    connections = []

    with open('mapSolarSystemJumps.csv.bz2', 'wb') as f:
        f.write(requests.get(mapjumps_url).content)

    open('mapSolarSystemJumps.csv', 'wb').write(
        bz2.open('mapSolarSystemJumps.csv.bz2', 'rb').read())

    with open('mapSolarSystemJumps.csv', encoding='UTF-8') as f:
        csv_file = csv.reader(f)
        next(csv_file)  # skip headers
        for row in csv_file:
            # fromsolarsystem = SolarSystem.objects.get(id=row[2])
            tosolarsystem = SolarSystem.objects.get(id=row[3])

            connections.append(SolarSystemConnection(
                fromsolarsystem_id=row[2],
                tosolarsystem_id=row[3],
                prefer_shortest=1,
                prefer_safest=1 if tosolarsystem.security_status >= 0.45 else 50000.0,  # High Sec
                prefer_less_safe=1 if tosolarsystem.security_status < 0.45 else 50000.0,  # Low/Null
            ))

    SolarSystemConnection.objects.bulk_create(connections, batch_size=500, ignore_conflicts=True)


def import_trig_data():
    TRIG_CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trigInvasionSystems.csv')
    trig_systems = []
    with open(TRIG_CSV_PATH, encoding='UTF-8') as f:
        csv_file = csv.reader(f)
        next(csv_file)  # skip headers
        for row in csv_file:
            trig_systems.append(TrigInvasion(
                system_id=row[0],
                status=row[1]
            ))

    TrigInvasion.objects.bulk_create(trig_systems, batch_size=500, ignore_conflicts=True)
