./asset folder: where we write index.jsx, App.jsx, Timer.jsx, shadcn etc react codes 

./static folder: here two kinds of contents are here:
1. ./index-bundle.jsx : this is the compiled file of the ./asset folder files by webpack. [see webpack.config.js]
2. ./static/firstApp : here, from the old Django-HTMX setup, static files are present. like css and images. they are refferenced in django like {%static ....%}


django creates its own for-deployment statcic files at ./django_bunnlde taking the for-development staic files from ./static upon running python manage.py collectstatic. [see settings.py]




===========================================

alias are set up at
1. webpack.config.js [used while bundling]
2. tsconfig.json [without here, import statements in ts files will be marked red in VS code]
3. components.json [when executing command on shadcn CLI, this tells shadcn where to install the packages.]

while declaring alias in any config files, don't use alias in the RHS. 


=============================================