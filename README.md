# Project Search
A simple little app that allows a user to search through mock products.  
The project is built entirely with Django, HTML, and CSS.

### Requirements
* Python 3.5 or newer
* PIP

### Setup Instructions
DISCLAIMER: I haven't tested these setup instructions, but they're pretty standard.
* clone the repository
* set up a new virtual environment if you'd like
* run pip install -r requirements.txt
* cd into the productsearch/ directory
* run python manage.py runserver
* visit 127.0.0.1:8000/products in your web browser

If you get an error at the second to last step, you might need to run 
python manage.py makemigrations and python manage.py migrate.

Once again, I'm sorry if these instructions are horribly wrong - I haven't tested them myself.