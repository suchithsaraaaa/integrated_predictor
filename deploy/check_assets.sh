#!/bin/bash
echo "🎥 CHECKING VIDEO ASSETS..."

echo " -> Content of /var/www/nestiq/:"
ls -F /var/www/nestiq/

echo " -> Content of /var/www/nestiq/videos/ (If exists):"
if [ -d "/var/www/nestiq/videos" ]; then
    ls -l /var/www/nestiq/videos/
else
    echo "❌ /videos directory MISSING in webroot!"
fi

echo " -> Content of /var/www/nestiq/assets/:"
if [ -d "/var/www/nestiq/assets" ]; then
    ls -F /var/www/nestiq/assets/ | grep mp4 || echo "No mp4 in assets."
fi

echo "=========================================="
echo "If directory is missing, we need to check if 'npm run build' actually created it."
echo "=========================================="
