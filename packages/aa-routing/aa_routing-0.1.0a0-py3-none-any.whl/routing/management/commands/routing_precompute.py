from networkx import to_dict_of_dicts

from django.core.management.base import BaseCommand

from routing.graph import build


class Command(BaseCommand):
    help = ""

    def handle(self, *args, **options):

        G = build()

        with open("routing_output.txt", "w") as f:
            f.write(str(to_dict_of_dicts(G)))
