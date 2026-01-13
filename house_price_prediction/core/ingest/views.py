from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import ingest_data_for_country

@api_view(["POST"])
def ingest_country_data(request):
    """
    Trigger data ingestion.
    Body: {"country_code": "IN", "count": 100}
    """
    country_code = request.data.get("country_code", "US")
    count = int(request.data.get("count", 100))
    
    try:
        total = ingest_data_for_country(country_code, count)
        return Response({
            "status": "success", 
            "message": f"Ingested {total} records for {country_code}"
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)
