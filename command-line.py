from docutils.nodes import Root
from mimetypes import init
mkdir djangogirls
cd djangogirls

## THE VIRTUAL ENVIRONEMENT ####################################################

# make a virtualenv called myvenv
python -m venv myvenv
#start your vitual environement
source myvenv/bin/activate

## DJANGO ######################################################################

# install Django using pip
pip install django==1.9.4

# start a new Django project
django-admin startproject monsiteweb .

# change the 'monsiteweb/setting.py' file
# -- time zone
> TIME_ZONE = 'Europe/Paris'
# -- path for static files (css)
> STATIC_URL = '/static/'
> STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# -- setup a database (already setup in the file)
> DATABASES = {
>     'default': {
>         'ENGINE': 'django.db.backends.sqlite3',
>         'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
>     }
> }

# create a database for your blog
python manage.py migrate

# start the web server
python manage.py runserver

# check that your website is running
# in your browser, enter the address :
http://127.0.0.1:8000/

# CONGRATS' ! you've juste created your first website
# and run it using a web server

## DJANGO MODELS ###############################################################

# A model in Django is a special kind of object : it is save in the database
# We will be using a SQLite database to store our data (the default Django
# database adapter, it will be enough for us right now)

# create an application (a separate application inside our projetc)
# -- open a new Tab in your terminal and type de following command
source myvenv/bin/activate
# -- create the application
python manage.py startapp monblog

# tell Django that it should use your new application
# change the 'monsiteweb/setting.py' file, add the last line :
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'monblog',
]

# create a blog post model, in the 'monblog.models.py' file :
# remove everything from it and write the following code
> from django.db import models
> from django.utils import timezone
> 
> class Post(models.Model):
>     author = models.ForeignKey('auth.User')
>     title = models.CharField(max_length=200)
>     text = models.TextField()
>     created_date = models.DateTimeField(
>             default=timezone.now)
>     published_date = models.DateTimeField(
>             blank=True, null=True)
>     
>     def publish(self):
>         self.published_date = timezone.now()
>         self.save()
>     
>     def __str__(self):
>         return self.title

# create tables for models in your database
python manage.py makemigrations monblog

# Django prepared for us a migratin file that we have to apply now
# to our database.
python manage.py migrate monblog

# CONGRATS' ! Your Post model is now in your database. Next we will see it !

## DJANGO ADMIN ################################################################

# open the 'monblog/admin.py' file and replace its content with this :
# we import the Post model defined before. to make it visible on the admin page,
# we need to register the model (last line of code)
> from django.contrib import admin
> from .models import Post
> 
> admin.site.register(Post)

# Go the your browser and type the address :
http://127.0.0.1:8000/admin/

# to log in, create a superuser, one who has control over everything on the site
python manage.py createsuperuser
> username : root
> email address : rakho.myriam@gmail.com
> password : mosaFL55-34ART

# return to your brower and log in with your superuser's credentials

# in the Django admin dashboard, add Posts
# make sure that at least 2 or 3 posts (but not all) have the publish date set

## DEPLOY YOUR WEBSITE #########################################################

# Until now, your project was only available on your computer.
# Now you will learn how to deploy it !
# Deploying is the process of publishing your application on the Internet
# so people can finally go and see your app

## PythonAnywhere
# A website has to be located on a server. There are a lot of server providers
# available on the internet. We will use one that has a relatively simple
# deployment process : PythonAnywhere. PythonAnywhere is free for small
# applications that don't have too many visitors so it'll definitely be enough
# for you.

## GitHub
# The other external service we'll be using is GitHub, a code hosting service.

## 3 places
# These three places will be important to you.
# -- Your local computer will be the place where you do development and testing
# -- When you're happy with the changes, you'll place a copy of your program on GitHub
# -- Your website will be on PythonAnywhere and you will update it by getting
# a new copy of your code from GitHub

## GIT
# -- installing Git
# On Mac OS : Download it from git-scm.com and just follow the instructions
# On Linux : sudo apt-get install git

# -- start a Git repository
# initializing the git repository is something you only need to do one per project
git init
git config --global user.name "root"
git config --global user.email rakho.myriam@gmail.com

# Git will track changes to all the files and folders in this directory,
# but there are some files we want it to ignore. We do this by creating
# a file called .gitignore in the 'djangogirls' directory. Open up your editor
# and create a new file with the following contents:
> *.pyc
> __pycache__
> myvenv
> db.sqlite3
> /static
> .DS_Store

# The 'db.sqlite3' file is your local database, where all your posts are stored.
# We don't want to add this to your repository, because your website on PythonAnywhere
# is going to be using a different database.
# That database could be SQLite, like your development machine, but usually,
# you will use one called MySQL which can deal with a lot more site visitors
# than SQLite.
# Either way, by ignoring your SQLite database for the GitHub copy, it means
# that all of the posts you created so far are going to stay and only be
# available locally, but you're gonna have to add them again on production.
# You should think of your local database as a good playground where you can test
# different things and not be afraid that you're going to delete your real
# posts from your blog.

# whenever you find yourself unsure of what has changed
# (this will help stop any surprises from happening, such as wrong files being
# added of commited)
git status

# save your changes
git add -A .
git commit -m "My Django Girls app, first commit"




################################################################################