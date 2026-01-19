from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ml.feature_engineering.build_features import build_feature_vector
from ml.predict import predict_price
from properties.services.area_insights import get_area_insights
from properties.services.crime import get_or_create_crime_metric
from properties.services.traffic import get_or_update_traffic_metric
from properties.services.accessibility import get_or_update_accessibility_metric

from django.views.decorators.csrf import csrf_exempt

@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        "status": "ok",
        "message": "House Price Prediction API is running"
    })

@csrf_exempt
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def warmup_location(request):
    try:
        latitude = float(request.data["latitude"])
        longitude = float(request.data["longitude"])
        get_area_insights(latitude, longitude)
        return Response({"status": "warmed"})
    except Exception:
        return Response({"status": "error"}, status=500)


@csrf_exempt
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def predict_price_view(request):
    data = request.data
    try:
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])
        selected_year = int(data["year"])
        CURRENT_YEAR = 2025

        # 1. GET LOCATION DATA (Insights drive the price!)
        from properties.services.area_insights import get_area_insights
        area_insights = get_area_insights(latitude, longitude)
        
        # 2. DETERMINE REGION & MULTIPLIERS (GLOBAL SUPPORT)
        from properties.services.location_intelligence import get_location_economics
        
        econ = get_location_economics(latitude, longitude)
        currency = econ['currency']
        market_multiplier = econ['mult']
        growth_factor = econ['growth']

        # 3. CALCULATE INFRASTRUCTURE SCORE (The "Equation")
        # User Logic: Schools/Hospitals/Crime -> Price
        schools = area_insights['schools']['count']
        hospitals = area_insights['hospitals']['count']
        crime_pct = area_insights['crime_rate_percent'] # e.g. 15

        # Calibration:
        # Schools: +0.5% per school (max cap useful)
        # Hospitals: +1.0% per hospital
        # Crime: -1.0% per percentage point of crime
        
        infra_bonus = (schools * 0.005) + (hospitals * 0.01)
        crime_penalty = (crime_pct / 100.0) * 1.5 # Stronger penalty
        
        # Base factor starts at 1.0
        # If High Crime (20%) -> -0.30
        # If Good Infra (10 schools, 5 hosp) -> +0.05 + 0.05 = +0.10
        quality_multiplier = 1.0 + infra_bonus - crime_penalty
        
        # Clamp to avoid extreme outliers (0.5x to 1.5x of base regional price)
        quality_multiplier = max(0.5, min(quality_multiplier, 1.5))
        
        print(f"   [LOGIC] Loc: {latitude},{longitude} | S:{schools} H:{hospitals} C:{crime_pct}% | QualMult: {quality_multiplier:.2f}")

        # 4. PREDICT RAW (Base Model)
        features_future = build_feature_vector(
            latitude=latitude,
            longitude=longitude,
            area_sqft=float(data["area_sqft"]),
            bedrooms=int(data["bedrooms"]),
            bathrooms=int(data["bathrooms"]),
            year=selected_year,
        )
        raw_price_future = predict_price(features_future)[0]

        features_current = build_feature_vector(
            latitude=latitude,
            longitude=longitude,
            area_sqft=float(data["area_sqft"]),
            bedrooms=int(data["bedrooms"]),
            bathrooms=int(data["bathrooms"]),
            year=CURRENT_YEAR,
        )
        raw_price_current = predict_price(features_current)[0]

        # 5. FINAL CALCULATION
        # Price = Base_Model * Regional_Cost * Quality_Score
        final_current_price = raw_price_current * market_multiplier * quality_multiplier
        # Future also applies growth
        final_future_price = raw_price_future * market_multiplier * growth_factor * quality_multiplier

        # 6. TREND
        trend_data = []
        for y in range(2021, 2030):
             fts = build_feature_vector(
                latitude=latitude,
                longitude=longitude,
                area_sqft=float(data["area_sqft"]),
                bedrooms=int(data["bedrooms"]),
                bathrooms=int(data["bathrooms"]),
                year=y,
            )
             raw = predict_price(fts)[0]
             
             # Apply logic
             adjusted = raw * market_multiplier * quality_multiplier
             if y > 2025:
                 adjusted *= growth_factor
             
             trend_data.append({"year": y, "price": round(float(adjusted), 2)})

        response = Response({
            "predicted_price": round(float(final_future_price), 2),
            "current_price": round(float(final_current_price), 2),
            "currency": currency,
            "area_insights": area_insights,
            "year": selected_year,
            "price_trend": trend_data
        })
        return response

    except Exception as e:
        return Response({"error": str(e)}, status=500)
