#!/bin/bash
echo "💰 VERIFYING PRICING LOGIC..."

TARGET_FILE="house_price_prediction/core/properties/api/views.py"

# 1. CHECK SOURCE CODE
echo " -> Checking $TARGET_FILE for new multipliers..."
if grep -q "market_multiplier = 3.5" "$TARGET_FILE"; then
    echo "✅ CODE UPDATED: Found multiplier 3.5 (Americas/UK)"
else
    echo "❌ CODE OUTDATED: Did not find multiplier 3.5"
    echo "   Current 9.0 lines:"
    grep "market_multiplier = 9.0" "$TARGET_FILE" || echo "   (None found?)"
fi

# 2. RESTART SERVICE
echo " -> Restarting Nestiq Service..."
sudo systemctl restart nestiq
sleep 2

# 3. TEST API (Local Curl)
echo " -> Testing Prediction API (Localhost)..."
# Sample payload for US/UK region to test multiplier
curl -X POST http://localhost/api/predict/ \
     -H "Content-Type: application/json" \
     -d '{
           "latitude": 51.5074, 
           "longitude": -0.1278,
           "area_sqft": 1000,
           "bedrooms": 2,
           "bathrooms": 1,
           "year": 2025
         }'
echo "" 
echo "=========================================="
echo "Check the 'predicted_price' above."
echo "=========================================="
