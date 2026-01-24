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
        # DEFENSIVE: Use .get() to prevent crashes on legacy cache data
        schools = area_insights.get('schools', {}).get('count', 5)
        hospitals = area_insights.get('hospitals', {}).get('count', 2)
        crime_pct = area_insights.get('crime_rate_percent', 10) # Default 10% if missing

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
        
        # DYNAMIC GROWTH FACTOR
        # Better area = Faster Growth. High Crime = Slower Growth.
        # We dampen the impact for growth (it shouldn't swing as wildly as price - reduced wt to 10%)
        growth_modifier = 1.0 + (infra_bonus * 0.1) - (crime_penalty * 0.1)
        # Clamp growth modifier (e.g. 0.95x to 1.05x of base growth)
        growth_modifier = max(0.95, min(growth_modifier, 1.05))
        
        final_growth_factor = growth_factor * growth_modifier
        
        # SAFETY: Hard Cap at 12% annual growth to prevent runaway projections
        final_growth_factor = min(final_growth_factor, 1.12)

        print(f"   [LOGIC] Loc: {latitude},{longitude} | QualMult: {quality_multiplier:.2f} | Growth: {final_growth_factor:.3f}")

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
        
        # Future Price = Current Price * (Growth ^ Years)
        years_diff = max(0, selected_year - CURRENT_YEAR)
        final_future_price = final_current_price * (final_growth_factor ** years_diff)

        # 6. TREND
        trend_data = []
        for y in range(2021, 2030):
             # For trend, we can just project from current price for simplicity and smoothness
             # logic: Price(Y) = Price(Current) * (Growth ^ (Y - Current))
             
             diff = y - CURRENT_YEAR
             if diff == 0:
                 price_y = final_current_price
             elif diff > 0:
                 price_y = final_current_price * (final_growth_factor ** diff)
             else:
                 # Backcast (Simulated via inverse growth)
                 price_y = final_current_price / (final_growth_factor ** abs(diff))
             
             trend_data.append({"year": y, "price": round(float(price_y), 2)})

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
