#!/bin/bash

# LiveReload server for browser hot reload
# Watches public/ directory for changes

echo "🔄 Starting LiveReload server..."
echo "   Watching: public/"

npx livereload public/ --wait 200 --extraExts 'html,css,js'
