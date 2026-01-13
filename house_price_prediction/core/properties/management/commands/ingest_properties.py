from django.core.management.base import BaseCommand
from properties.services.ingestion import ingest_properties


class Command(BaseCommand):
    help = "Ingest real-time property data using HomeHarvest"

    def add_arguments(self, parser):
        parser.add_argument("--location", type=str, required=True)
        parser.add_argument("--days", type=int, default=7)

    def handle(self, *args, **options):
        location = options["location"]
        days = options["days"]

        count = ingest_properties(location=location, past_days=days)

        self.stdout.write(
            self.style.SUCCESS(f"Ingested {count} properties for {location}")
        )
