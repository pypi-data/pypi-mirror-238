from networkx import DiGraph

from routing.models import SolarSystem, SolarSystemConnection

from .static_data import precomputed_graph


def build(static_cache: bool = False) -> DiGraph:
    if static_cache:
        G = DiGraph(precomputed_graph)
        return G
    else:
        G = DiGraph()
        for node in SolarSystem.objects.values_list("id", "security_status"):
            G.add_node(node[0], security_status=node[1], type="stargate")

        for edge in SolarSystemConnection.objects.values_list(
            "fromsolarsystem",
            "tosolarsystem",
            "prefer_shortest",
            "prefer_safest",
            "prefer_less_safe"
        ).all():
            G.add_edge(edge[0], edge[1], prefer_shortest=edge[2], prefer_safest=edge[3], prefer_less_safe=edge[4])

        return G
