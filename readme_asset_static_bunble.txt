./asset folder: where we write index.jsx, App.jsx, Timer.jsx etc react codes 

./static folder: here two kinds of contents are here:
1. ./index-bundle.jsx : this is the compiled file of the ./asset folder files by webpack. [see webpack.config.js]
2. ./static/firstApp : here, from the old Django-HTMX setup, static files are present. like css and images. they are refferenced like {%static ....%}


django creates its own for-deployment statcic files at ./django_bunnlde taking the for-development staic files from ./static upon running python manage.py collectstatic. [see settings.py]