#!/bin/bash
echo "💱 FIXING ECONOMIC LOGIC (EXCHANGE RATES)..."

# We completely replace the 'views.py' multiplier logic with a calibrated one.
# logic: (Model_INR * Quality_Ratio) / Exchange_Rate
# UK: ~15x value / 110 INR/GBP = 0.14
# US: ~12x value / 85 INR/USD = 0.14
# AU: ~10x value / 55 INR/AUD = 0.18
# IN: ~0.7 (Calibration adjustment)

TARGET_FILE="house_price_prediction/core/properties/api/views.py"

# Use python to rewrite the file content safely or block replacement
sudo cat > $TARGET_FILE <<EOF
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ml.feature_engineering.build_features import build_feature_vector
from ml.predict import predict_price
from properties.services.area_insights import get_area_insights

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

        # 1. PREDICT RAW (INR)
        features_future = build_feature_vector(
            latitude=latitude,
            longitude=longitude,
            area_sqft=float(data["area_sqft"]),
            bedrooms=int(data["bedrooms"]),
            bathrooms=int(data["bathrooms"]),
            year=selected_year,
        )
        # Raw model output is in Rupees (approx)
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

        # 2. DETERMINE REGION & MULTIPLIERS
        # Logic: Final = Raw_INR * (Value_Ratio / Exchange_Rate)
        
        currency = {"symbol": "$", "code": "USD"}
        market_multiplier = 0.14  # Default (approx US/Global)
        growth_factor = 1.0

        # India (INR)
        if 6 <= latitude <= 37 and 68 <= longitude <= 97:
            currency = {"symbol": "₹", "code": "INR"}
            market_multiplier = 0.6  # Calibration: 0.6x to fix "Too High"
            growth_factor = 1.05
            
            if 18.5 <= latitude <= 19.5 and 72.5 <= longitude <= 73.5: # Mumbai
                market_multiplier = 1.2  # Mumbai is expensive
            elif 12.5 <= latitude <= 13.5 and 77.0 <= longitude <= 78.0: # Blr
                market_multiplier = 0.8  

        # UK (GBP) - Exch ~110
        elif 49 <= latitude <= 61 and -8 <= longitude <= 2:
            currency = {"symbol": "£", "code": "GBP"}
            # Value ~15x Hyd, Exch ~110 => 15/110 = 0.136
            market_multiplier = 0.14
            growth_factor = 0.9

        # Europe (EUR) - Exch ~90
        elif 35 <= latitude <= 72 and -12 <= longitude <= 45:
             currency = {"symbol": "€", "code": "EUR"}
             # Value ~12x Hyd, Exch ~90 => 12/90 = 0.133
             market_multiplier = 0.13
             growth_factor = 0.95

        # Australia (AUD) - Exch ~55
        elif -45 <= latitude <= -10 and 110 <= longitude <= 155:
            currency = {"symbol": "A$", "code": "AUD"}
            # Value ~10x Hyd, Exch ~55 => 10/55 = 0.18
            market_multiplier = 0.18
            growth_factor = 1.1

        # Americas (USD) - Exch ~86
        elif 15 <= latitude <= 70 and -170 <= longitude <= -50:
             currency = {"symbol": "$", "code": "USD"}
             # Value ~12x Hyd, Exch ~86 => 12/86 = 0.14
             market_multiplier = 0.14
             growth_factor = 1.1

        # 3. APPLY LOGIC
        final_current_price = raw_price_current * market_multiplier
        final_future_price = raw_price_future * market_multiplier * growth_factor

        # 4. TREND
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
             
             # Apply simple scalar logic for trend
             adjusted = raw * market_multiplier
             if y > 2025:
                 adjusted *= growth_factor
             
             trend_data.append({"year": y, "price": round(float(adjusted), 2)})

        # 5. INSIGHTS
        area_insights = get_area_insights(latitude, longitude)

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
EOF

echo " -> Restarting Service..."
sudo systemctl restart nestiq
echo "✅ ECONOMICS FIXED."
