from typing import Dict, List

from routing.app_settings import corptools_active
from routing.models import SolarSystemConnection, TrigInvasion

if corptools_active():
    from corptools.models import MapJumpBridge


def include_corptools_jumpbridges():
    edges = []
    if corptools_active():
        for jb in MapJumpBridge.objects.values_list("from_solar_system_id", "to_solar_system_id").all():
            edges.append((
                jb.fromsolarsystem, jb.tosolarsystem,
                {'prefer_shortest': 1.0, 'prefer_safest': 1.0, 'prefer_less_safe': 1.0}))
    else:
        return edges

    return edges


def include_eve_scout(system: str = "thera") -> List[Dict]:
    edges = []
    if system == "thera":
        pass
    elif system == "turnur":
        pass
    return edges
    # return [(30100000, 30003841, {'prefer_shortest': 1.0, 'prefer_safest': 1.0, 'prefer_less_safe': 1.0})]


def avoid_edencom():
    edges = []
    for system in TrigInvasion.objects.filter(status__in=["fortress", "edencom_minor_victory"]).values_list("tosolarsystem", flat=True).all():
        for connection in SolarSystemConnection.objects.filter(to_solar_system=system):
            edges.append((
                connection.fromsolarsystem, connection.tosolarsystem,
                {'prefer_shortest': 50000.0, 'prefer_safest': 50000.0, 'prefer_less_safe': 50000.0}))

    return edges
