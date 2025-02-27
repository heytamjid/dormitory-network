./asset folder: where we write index.jsx, App.jsx, Timer.jsx etc

./static folder: here two kinds of contents are here:
1. ./index-bundle.jsx : this is the compiled file of the ./asset files by webpack. [see webpack.config.js]
2. ./static/firstApp : here, from the old Django-HTMX setup, static files are present. like css and images. they need to be moved to elsewhere.  