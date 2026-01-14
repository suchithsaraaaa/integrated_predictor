#!/bin/bash
echo "📋 CHECKING CONFIG SYNTAX..."
sudo nginx -t
echo "-------------------"
echo "If failed, dumping the file:"
cat /etc/nginx/sites-enabled/nestiq || echo "File not found"
