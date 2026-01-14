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
    """
    Triggers area insights fetching in the background (or synchronously 
    if no async worker) to populate the cache.
    """
    try:
        latitude = float(request.data["latitude"])
        longitude = float(request.data["longitude"])
        
        # This will trigger the fetch and cache it
        # Since we re-enabled the slow path, this might take 5-10s
        # BUT the user is busy watching the video wizard.
        get_area_insights(latitude, longitude)
        
        return Response({"status": "warmed"})
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@csrf_exempt
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

        # 1. Predict Future Price (Selected Year)
        features_future = build_feature_vector(
            latitude=latitude,
            longitude=longitude,
            area_sqft=float(data["area_sqft"]),
            bedrooms=int(data["bedrooms"]),
            bathrooms=int(data["bathrooms"]),
            year=selected_year,
        )
        print(f"[DEBUG] Features (Future): {features_future}") # Log features
        predicted_price_future = predict_price(features_future)[0]

        # 2. Predict Current Price (2025)
        features_current = build_feature_vector(
            latitude=latitude,
            longitude=longitude,
            area_sqft=float(data["area_sqft"]),
            bedrooms=int(data["bedrooms"]),
            bathrooms=int(data["bathrooms"]),
            year=CURRENT_YEAR,
        )
        predicted_price_current = predict_price(features_current)[0]

        # 3. GENERATE TREND DATA (2021 to 2029)
        trend_data = []
        for y in range(2021, 2030): # 4 years back, 4 years forward from 2025
            feats = build_feature_vector(
                latitude=latitude,
                longitude=longitude,
                area_sqft=float(data["area_sqft"]),
                bedrooms=int(data["bedrooms"]),
                bathrooms=int(data["bathrooms"]),
                year=y,
            )
            price = predict_price(feats)[0]
            trend_data.append({"year": y, "price": round(float(price), 2)})

        predicted_price_current = predict_price(features_current)[0]

        # 🔑 AREA INSIGHTS
        area_insights = get_area_insights(
            latitude=latitude,
            longitude=longitude
        )

        # 🔑 CURRENCY & REGIONAL MULTIPLIER DETECTION
        currency = {"symbol": "$", "code": "USD"}
        market_multiplier = 1.0
        growth_factor = 1.0 # Default Growth Modifier
        
        # Heuristic Bounding Boxes
        
        # 1. India (₹)
        if 6 <= latitude <= 37 and 68 <= longitude <= 97:
            currency = {"symbol": "₹", "code": "INR"}
            
                if 18.5 <= latitude <= 19.5 and 72.5 <= longitude <= 73.5:
                market_multiplier = 2.0 
                growth_factor = 1.2 # Mumbai grows faster
                print(f"[DEBUG] Region: MUMBAI (x2.0, Growth x1.2)")
            elif 12.5 <= latitude <= 13.5 and 77.0 <= longitude <= 78.0:
                market_multiplier = 1.2 
                growth_factor = 1.4 # Bangalore tech boom
                print(f"[DEBUG] Region: BANGALORE (x1.2, Growth x1.4)")
            elif 28.0 <= latitude <= 29.0 and 76.5 <= longitude <= 77.5:
                market_multiplier = 1.3
                growth_factor = 1.1
                print(f"[DEBUG] Region: DELHI (x1.3, Growth x1.1)")
            else:
                market_multiplier = 1.0 
                growth_factor = 1.05 # Emerging India
                print(f"[DEBUG] Region: INDIA GENERIC (x1.0, Growth x1.05)") 
            
        # 2. United Kingdom (£) 
        elif 49 <= latitude <= 61 and -8 <= longitude <= 2:
            currency = {"symbol": "£", "code": "GBP"}
            market_multiplier = 3.5 
            growth_factor = 0.8 # Mature market, slower growth
            print(f"[DEBUG] Region: UK (x3.5, Growth x0.8)")
            
        # 3. Europe (High-level Box) (€)
        elif 35 <= latitude <= 72 and -12 <= longitude <= 45:
             currency = {"symbol": "€", "code": "EUR"}
             market_multiplier = 3.0 
             growth_factor = 0.9
             print(f"[DEBUG] Region: EUROPE (x3.0, Growth x0.9)")

        # 4. Australia (A$)
        elif -45 <= latitude <= -10 and 110 <= longitude <= 155:
            currency = {"symbol": "A$", "code": "AUD"}
            market_multiplier = 3.0
            growth_factor = 1.15
            print(f"[DEBUG] Region: AUSTRALIA (x3.0, Growth x1.15)")
            
        # 5. New Zealand (NZ$)
        elif -48 <= latitude <= -33 and 165 <= longitude <= 180:
             currency = {"symbol": "NZ$", "code": "NZD"}
             market_multiplier = 2.5
             growth_factor = 1.1
             
        # 6. Americas (Default USD)
        elif 15 <= latitude <= 70 and -170 <= longitude <= -50:
             market_multiplier = 3.5 
             growth_factor = 1.1 # Steady US growth
             print(f"[DEBUG] Region: AMERICAS (x3.5, Growth x1.1)")

        # APPLY MULTIPLIER
        # Only apply growth factor to the FUTURE price
        final_current_price = predicted_price_current * market_multiplier
        
        # Future price = Raw Future * Market Multiplier * Growth Multiplier
        # This biases the slope of the curve
        final_future_price = predicted_price_future * market_multiplier * growth_factor
        
        # Re-calc trend with multiplier
        final_trend = []
        for item in trend_data:
            # Apply progressive growth to the trend curve
            # Year 2025 is base. 
            # 2029 should be fully affected by growth_factor.
            # 2021 should be less affected (or inverse).
            
            # Simple approach: Apply constant multipliers for now, 
            # but scale the price by the growth factor relative to distance from now?
            # Actually, let's just apply the scalar.
            # Ideally we'd warp the time series, but simple scalar is enough to show difference %
            
            # If item year > 2025: apply growth_factor
            # If item year <= 2025: don't apply (or apply inverse?)
            # Let's just apply it to future years for the 'compare' diff to show up.
            
            p = item["price"] * market_multiplier
            if item["year"] > 2025:
                p *= growth_factor
            
            final_trend.append({"year": item["year"], "price": round(p, 2)})

        print(f"[DEBUG] Final Price: {final_future_price} (Multiplier: {market_multiplier})")

        response = Response({
            "predicted_price": round(float(final_future_price), 2),
            "current_price": round(float(final_current_price), 2),
            "currency": currency,
            "area_insights": area_insights,
            "year": selected_year,
            "price_trend": final_trend
        })
        response["X-Model-Version"] = "v2_Global_Multipliers"
        return response

    except KeyError as e:
        return Response(
            {"error": f"Missing field: {str(e)}"},
            status=400
        )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=500
        )
