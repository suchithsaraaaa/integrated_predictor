#!/bin/bash
echo "🕵️ FRONTEND AUDIT: Investigating 'Forbidden' Error"
echo "==================================================="

WEB_ROOT="/var/www/nestiq"
DIST_DIR="/home/ubuntu/integrated_predictor/nestiq-predict-main/dist"

echo "1. 📂 Content of Web Root ($WEB_ROOT):"
ls -laR "$WEB_ROOT"

echo "---------------------------------------------------"
echo "2. 📂 Content of Build Dir ($DIST_DIR):"
if [ -d "$DIST_DIR" ]; then
    ls -la "$DIST_DIR"
else
    echo "❌ DIST DIRECTORY MISSING!"
fi

echo "---------------------------------------------------"
echo "3. 🧠 Memory Check (Did build crash?):"
free -h

echo "---------------------------------------------------"
echo "4. 🧪 Write Test:"
echo "<h1>Test File</h1>" | sudo tee "$WEB_ROOT/test.html" > /dev/null
echo "   Written test.html. Curl test:"
curl -I "http://localhost/test.html"

echo "==================================================="
