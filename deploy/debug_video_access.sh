#!/bin/bash
echo "🎥 DEBUGGING VIDEO ACCESS..."

# 1. CHECK THE JS CODE (Did the rebuild work?)
echo " -> Grepping deployed JS for old path '/assets/videos/'..."
# If we find this string, it means the old code is still there.
if grep -r "/assets/videos/" /var/www/nestiq/assets/; then
    echo "❌ FOUND OLD PATH! The frontend rebuild did NOT update the code."
    echo "   (You need to rerun: sudo bash deploy/rebuild_frontend.sh)"
else
    echo "✅ OLD PATH GONE. The code matches the fix."
fi

# 2. CHECK LOCAL ACCESS (MIME Type)
echo " -> Curling video from localhost..."
curl -I http://localhost/videos/home.mp4

echo "=========================================="
echo "If the JS check failed (❌), RUN THE REBUILD SCRIPT AGAIN."
echo "If the Curl check failed (404), the file is missing."
echo "=========================================="
