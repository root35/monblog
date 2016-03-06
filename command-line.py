from docutils.nodes import Root
from mimetypes import init
from cgitb import text
from warnings import onceregistry
from jinja2.exceptions import TemplatesNotFound
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

# *PythonAnywhere
# A website has to be located on a server. There are a lot of server providers
# available on the internet. We will use one that has a relatively simple
# deployment process : PythonAnywhere. PythonAnywhere is free for small
# applications that don't have too many visitors so it'll definitely be enough
# for you.

# *GitHub
# The other external service we'll be using is GitHub, a code hosting service.

# *3 places
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

# -- save your changes
git add -A .
git commit -m "My Django Girls app, first commit"

# -- push your code to GitHub
# --- go to GitHub.com. sign up for a new, free user account
# --- create a new repository
nom du blog : monblog
# --- leave the "initialise with a README" tickbox unchecked, leave the .gitignore
# option blank (we've done that manually) and leave the License as None.

# -- on the next screen, you'll be shown your repo's clone URL.
# choose the "HTTPS" version, copy it, and we'll paste it into the terminal shortly
https://github.com/root35/monblog.git

# -- now we need to hook up the Git repository on your computer to the one on GitHub.
git remote add origin https://github.com/root35/monblog.git
git push -u origin master

# your code is now on GitHub

## Set up your blog on PythonAnywhere

# -- go to www.pythonanywhere.com and sign up for a free "Beginner" account
# -- in your dashboard "Consoles" page, choose the option to start a "Bash" console.
# that's the PythonAnywhere version of a console, just like the one on your computer.
# PythonAnywhere is based on Linux, so if you're on Windows, the console will look
# a little different from the one on your computer.

# -- pull down your code from GitHub onto PythonAnywhere by creating a "clone"
# of your repository.
# in the PythonAnywhere console :
git clone https://github.com/root35/monblog.git

# the previous command will pull down a copy of your code onto PythonAnywhere.
# Check it out by typing
tree monblog

# -- create a virtualenv on PythonAnywhere
cd monblog
virtualenv --python=python3.4 myvenv
source myvenv/bin/activate
pip install django==1.9.4

# -- Collecter les fichiers statiques
python manage.py collectstatic

# -- Create the database on PythonAnywhere
# Another thing that's different between your own computer and the server
# is that it uses a different database. So the user accounts and posts can be
# different on the server and on your computer.
# We can initialise the database on the server just like we did the one on
# your own computer
python manage.py migrate
python manage.py createsuperuser
> username : root
> email address : rakho.myriam@gmail.com
> password : mosaFL55-34ART

# -- Push your blog as a web app
# - Now our code is on PythonAnywhere, our virtualenv is ready, and the database
# is initialised. We're ready to publish it as a web app !
# - Click back to the PythonAnywhere dashboard by clicking on its logo, and go click
# on the 'Web' tab. Finally, hit 'Add a new web app'.
# - After confirming your domain name, choose 'manual configuration'
# (not the "Django" option) in the dialog.
# - Next choose 'Python 3.4' and click 'Next' to finish the wizard.
# !! Make sure you choose the "Manual configuration" option, not the "Django" one.

# -- setting the virtualenv
# - You'll be taken to the PythonAnywhere config screen for your webapp, which is
# where you'll need to go whenever you want to make changes to the app on the server.
# - In the 'Virtualenv' section, click the red text that says "Enter the path
# to a virtualenv", and enter :
/home/root35/monblog/myvenv/
# Click the blue box with the check mark to save the path before moving on.
# PS : If you make a mistake in your username, PythonAnywhere will show you
# a little warning.

# -- Configure the WSGI file
# Django works using the "WSGI protocol", a standard for serving websites using
# Python, which PythonAnywhere supports. The way we configure PythonAnywhere
# to recognise our Django blog is by editing a WSGI configuration file.
# - Click on the "WSGI configuration file" link, in the 'Code' section.
# It'll be named something like
/var/www/root35_pythonanywhere_com_wsgi.py
# and you'll be taken to an editor
# - Delete all the contents and replace them with something like this :
> import os
> import sys
> 
> path = '/home/root35/monblog'
> if path not in sys.path:
>     sys.path.append(path)
> 
> os.environ['DJANGO_SETTINGS_MODULE'] = 'monsiteweb.settings'
> 
> from django.core.wsgi import get_wsgi_application
> from django.contrib.staticfiles.handlers import StaticFilesHandler
> application = StaticFilesHandler(get_wsgi_application())

# - This file's job is to tell PythonAnywhere where our web app lives and what
# the Django settings file's name is.
# - The 'StaticFilesHandler' is for dealing with our CSS. This is taken care of
# automatically for you during local development by the 'runserver' command.
# You'll find out a bit more about static files later in the tutorial, when we edit
# the CSS for our site.
# - Hit 'Save' and then go back to the 'Web' tab
# - We're all done! Hit the big green 'Reload' button and you'll be able to go view
# your application. You'll find a link to it at the top of the page.

## YOUR ARE LIVE!

# The default page for your site should say "Welcome to Django", just like it does
# on your local computer. 

# -- Try adding "/admin/" to the end of the URL, and you'll be taken to the admin
# site. Log in with the username and password, and you'll see you can add new Posts
# on the server.

# -- Once you have a few posts created, you can go back to your local setup
# (not PythonAnywhere). From here you should work on your local setup to make changes.
# This is a common workflow in Web development :
# - make changes locally,
# - push those changes to GitHub,
# - pull your changes down to your live Web server.
# This allows you to work and experiment without breaking your live Web site.

## DJANGO URLs #################################################################

## The 'monsiteweb/urls.py' file :

# Django already put something here for you.
# The admin URL, which you visited in previous chapter, is already here:
url(r'^admin/', include(admin.site.urls))
# It means that for every URL that starts with 'admin/', Django will find
# a corresponding view. In this case, we're including a lot of admin URLs
# so it isn't packed into this small file -- it's more readable and cleaner
# like that.

## REGEX

# Do you wonder how Django matches URLs to view ?
# Django uses 'regex', short for "regular expressions". Regex has a lot of rules
# that form a search pattern. In this case, we will only need a limited subset
# of rules to express the pattern we are looking for, namely :
^   for beginning of the text
$   for end of the text
\d  for a digit
+   to indicate that the previous item should be repeated at least once
()  to capture part of the pattern
# Anything else in the pattern will be taken literally.
# Now imagine you have a website with the address like that :
http://www.monsiteweb.com/post/12345/
# where '12345' is the number of your post. Writing separate views for all
# the post numbers would be really annoying. With regular expressions, we can
# create a pattern that will match the url and extract the number for us :
^post/(\d+)/$
# Let's break it down piece by piece to see what we are doing here :
^post/  is telling Django to take anything that has 'post/' at the beginning of
        the url
(\d+)   means that there will be a number (one or more digits) and that we want
        the number captured and extracted
/       tells django that another '/' character should follow
$       then indicates the end of the URL meaning that only strings ending with
        the '/' will match this pattern

## YOUR FIRST DJANGO URL

# Time to create our first URL. We want 'http://127.0.0.1:8000/' to be a homepage
# of our blog and display a list of posts.
# We also want to keep the 'monsiteweb/urls.py' file clean, so we will import
# urls from our 'monblog' application to the main 'monsiteweb/urls.py' file.
# In the 'monsiteweb/urls.py' file, add a second line :
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('monblog.urls')),
]
# Django will now redirect anything that comes into 'http://127.0.0.1:8000/'
# to 'monblog/urls' and look for further instructions here.
# When writing regular expressions in Python, it is always done with 'r' in front
# of the string. This is a helpful hint for Python that the string may contain
# special characters that are not meant for Python itself, but for the regular
# expression instead.

## monblog/urls.py

# Create a new 'monblog/urls.py' empty file. Add these two first lines :
from django.conf.urls import url
from . import views
# - Here we're importing Django's function 'url' and all of our 'views'
# from 'monblog' application (we don't have any yet, but we will get to that
# in a minute).
# - After that, we can add our first URL pattern :
urlpatterns = [
    url(r'^$', views.post_list, name='post_list')
]
# - As you can see, we're now assigning a 'view' called 'post_list' to '^$' URL.
# - This regular expression will match '^' (a beginning) followed by '$' (an end),
# so only an empty string will match. That's correct because in Django URL
# resolvers, 'http://127.0.0.1:8000/' is not a part of the URL. This pattern
# will tell Django that 'views.post_list' is the right place to go if someone
# enters your website at the 'http://127.0.0.1:8000/' address.
# - The last part "name='post_list'" is the name of the URL that will be used
# to identify the view. This can be the same as the name of the view, but it
# can also be something completely different. We will be using the named URLs
# later in the project, so it is important to name each URL in the app.
# We should also try to keep the names of URLs unique and easy to remember.

# - add the 'monblog/urls.py' file to GitHub :
git add monblog/urls.py
git commit -m 'First Django URL. Adding the monblog/urls.py file'
git push origin master
# - pull your changes down to your live Web server :
#  - in the 'Files' tab, upload/refresh all the new files 
#  - then in the 'Web' tab, click on the green "Reload..." button
#  - then open the url "root35.pythonanywhere.com" into a new tab


## DJANGO VIEWS ################################################################

# A 'view' is a place where we put the "logic" of our application. It will
# request information from the 'model' you created before and pass it to a
# 'template'. Views are just Python functions that are a little bit more
# complicated than the ones we wrote in the 'Introduction to Python' chapter.
# 'Views' are placed in the 'views.py' file. We will add our 'views' to
# the 'monblog/views.py' file.

## THE 'monblog/views.py' FILE

# -- Open up this file and see what's in there :
from django.shortcuts import render
# The simplest 'view' can look like this :
# we create a function called 'post_list' that takes 'request' and 'return'
# a funciton 'render' that will render (put together) our template
# 'monblog/post_list.html'
def post_list(request):
    return render(request, 'monblog/post_list.html', {})

# add the 'monblog/views.py' file to GitHub :
git add monblog/views.py
git commit -m 'First Django view. Adding the monblog/views.py file'
git push origin master
# - pull your changes down to your live Web server :
#  - in the 'Files' tab, upload/refresh all the new files 
#  - then in the 'Web' tab, click on the green "Reload..." button
#  - then open the url "root35.pythonanywhere.com" into a new tab

## HTML ########################################################################

## WHAT'S A TEMPLATE ?

# - A template is a file that we can re-use to present different information in
# a consistent format. For example, you could use a template to help you write
# a letter, because although each letter might contain a different message and
# be addressed to a different person, they will share the same format.
# - A Django template's format is described in HTML.

## YOUR FIRST TEMPLATE

# Creating a template means creating a template file. Templates are saved in a
# 'monblog/templates/monblog' directory.
# -- so first create a directory called 'templates' : 
mkdir monblog/templates
# -- then create another directory called 'monblog' inside : 
mkdir monblog/templates/monblog
# You might wonder why we need two directories both called 'monblog'. As you will
# discover later, this is simply a useful naming convention that makes life easier
# when things start to get more complicated.

# Now we create a 'post_list.html' file (just leave it blank for now) inside
# the 'monblog/templates/monblog' directory
echo " " > monblog/templates/monblog/post_list.html

git add monblog/templates/monblog/post_list.html
git commit -m 'First template. Adding the monblog/templates/monblog/post_list.html file'
git push origin master
# - pull your changes down to your live Web server :
git push
# or
git pull

# -- See how your website looks now : http://127.0.0.1:8000/
# No errors anymore : your page appears completely blank
# However, your website isn't actually publishing anything except an empy page,
# because your template is empty too.

# -- Add the following to your template file



################################################################################