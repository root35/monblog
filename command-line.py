from docutils.nodes import Root, status
from mimetypes import init
from cgitb import text
from warnings import onceregistry
from jinja2.exceptions import TemplatesNotFound
from telnetlib import STATUS
from tkinter.tix import Shell
from pygments.lexers.templates import CssDjangoLexer
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

# -- Complete the your template file

## DEPLOY !

# -- commit and push your code up to GitHub
# - see what files have changed since you last deployed (run these commands locally) :
git status
# - in the 'djangogirls' directory, include all the changes within it :
# (with the -A option, git will recognize if you've deleted files, by default
# it only recognizes new/modified files)
git add -A .
# - Before we upload all the files, let's check what 'git' will be uploading
# (all the files that git will upload should now appear in green) :
git status
# - now, it's time to tell it to save in its history, by giving it a 'commit' message
# where you describe what you've changed (with double quotes !)
git commit -m "Changed the HTML for the site."
# - once you've done that, upload (or push) your changes up to GitHub :
git push

# -- pull your new code down to PythonAnywhere, and reload your webb app :
# - in your brower, in PythonAnywhere, go to your Bash console (or start
# a new one). Then, run :
cd ~/monblog
(myvenv)$ git pull
# and watch your code get downloaded. If you want to check that it's arrived,
# you can hope over to the 'File' tab and view your code on PythonAnywhere.
# - finally, hop on over to the 'Web' tab and hit 'Reload' on your web app.
# - open/refresh your web app on the server, changes should be visible :
http://root35.pythonanywhere.com

# - if you have an error "Please commit your changes or stash them before
# you can merge" or "Please move or remove them before you can merge"
# about any given file, for example "monblog/views.py", just run the following
# for each one of the files (in the PythonAnywhere console) :
git add monblog/views.py
git add monsiteweb/urls.py
git add monblog/urls.py
# then rerun :
(myvenv)$ git pull

################################################################################

# website locally :
http://127.0.0.1:8000/
# website on the server :
http://root35.pythonanywhere.com

## DJANGO ORM AND QuerySets ####################################################

# A QuerySet is a list of objects of a given Model. QuerySet allows you to read
# the data from the database, filter it and order it.

## DJANGO SHELL
# Open up your local console (not on PythonAnywhere) and type this command:
python manage.py shell
# The effect should be this:
(InteractiveConsole)
>>>
# You're now in Django's interactive console. It's just like Python prompt
# but with some additional Django magic. You can use all the Python commands
# here too, of course.

## ALL OBJECTS
# Let's try to display all or our posts first. You can do that with
# the following command:
>>> Posts.objects.all()
Traceback (most recent call last):
    File "<console>", line 1, in <module>
NameError: name 'Post' is not defined
# An error showed up. It tells us that there is no Post, and it's correct
# because we forgot to import it first
>>> from monblog.models import Post
# This is simple: we import model 'Post' from 'monblog.models'.
# Now let's try displaying all posts again:
>>> Posts.objects.all()
[<Post: my post title>, <Post: another post title>]
# It's a list of the posts we created earlier! We created them using
# the Django admin interface. But now we want to create new Posts using Python.

## CREATE OBJECT
# This is how your create a new Post object in database:
>>> Post.objects.create(author=me, title='Sample title', text='Test')
# But we have one missing ingredient here: 'me'. We need to pass an instance of
# 'User' model as an author. How to do that ?
# Let's import User model first:
>>> from django.contrib.auth.models import User
# What users do we have in our database ?
>>> User.objects.all()
[<User: root>]
# It's the superuser we created earlier. Let's get an instance of the user now:
me = User.objects.get(username='root')
# We now 'get' a 'User' with a 'username' that equals to 'root'.
# Now we can finally create our post:
>>> Post.objects.create(author=me, title='Sample title', text='Test')
# Now check if it worked:
>>> Post.objects.all()
[<Post: my post title>, <Post: another post title>, <Post: Sample title>]
# There it is, one more post in the list !

# (the full command set is:)
>>> from monblog.models import Post
>>> Posts.objects.all()
>>> from django.contrib.auth.models import User
>>> User.objects.all()
me = User.objects.get(username='root')
>>> Post.objects.create(author=me, title='Sample title', text='Test')
>>> Post.objects.all()

## ADD MORE POSTS
# You can now have a little fun and add more posts to see how it works.
# Add 2-3 more and go ahead to the next part.

## FILTERING OBJECTS
# A big part of QuerySets is an ability to filter them. Let's say we want to find
# all posts User 'roor' authored. We will use 'filter' instead of 'all' in
# 'Post.objects.all()'. In parentheses, we will state what condition(s) a blog
# post needs to meet to end up in our queryset. In our situation, it is 'author'
# that is equal to 'me'. The way to write it in Django is: 'author=me'.
# - Now our piece of code looks like this:
>>> Post.objects.filter(author=me)
[<Post: Sampletitle>, <Post: Post number 2>, <Post: My 3rd post!>, <Post: 4th title of post>]
# - Or maybe we want to see all the posts that contain a word 'title'
# in the 'title' field ?
>>> Post.objects.filter(title__contains='title')
[<Post: Sampletitle>, <Post: Sampletitle2>, <Post: Sampletitle3>, <Post: Sampletitle4>, ]
# the 2 underscore characters '__' between 'title' and 'contains' :
# Django's ORM uses this rule to separate field names ("title") and operations
# or filters ("contains"). If you only use one underscore, you'll get an error
# like "FieldError: Cannot resolve keyword title_contains".
# - You can also get a list of all published posts. We do it by filtering all
# the posts that have 'published_date' set in the past:
>>> from django.utils import timezone
>>> Post.objects.filter(published_date__lte=timezone.now())
[<Post: Hello Third>, <Post: Hello Fourth>]
# Unfortunately, the post we added from the Python console is not published yet.
# We can change that! First get an instance of a post we want to publish:
>>> post = Post.objects.get(title="Sampletitle")
# And then publish it with our 'publish' method:
>>> post.publish()
# Now try to get list of published posts again:
>>> Post.objects.filter(published_date__lte=timezone.now())
[<Post: Hello Third>, <Post: Hello Fourth>, <Post: Sampletitle>]

## ORDERING OBJECTS
# QuerySet also allow you to order the list of objects. Let's try to order them
# by 'created_date' field:
>>> Post.objects.order_by('created_date')
[<Post: Hello First>, <Post: Hello Second>, <Post: Hello Third>,
<Post: Hello Fourth>, <Post: Sampletitle>, <Post: Sampletitle2>,
<Post: Sampletitle3>, <Post: Sampletitle4>]
# We can also reverse the ordering by adding '-' at the beginning:
>>> Post.objects.order_by('-created_date')

## CHAINING QUERYSETS
# You can also combine QuerySets by chaining them together:
>>> Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
[<Post: Hello Third>, <Post: Hello Fourth>, <Post: Sampletitle>]
# This is really powerful and lets you write quite complex queries.

## YOU'RE NOW READY FOR THE NEXT PART!
# To close the shell, type this:
>>> exit()
$

## DYNAMIC DATA IN TEMPLATES ###################################################

# We have different pieces in place:
# - the 'Post'model in 'models.py'
# - we have 'post_list' in 'views.py'
# - and the template added
# But how will we actually make our posts appear in our HTML template?
# Because that is what we want to do: take some content (models saved in the
# database) and disply it nicely in our template.
# This is exactly what 'views' are supposed to do: connect models and templates.
# In our 'post_list' view, we will need to take models we want to display and
# pass them to the template. In a view, we decide what (model) will be displayed
# in a template.
# So how will we achieve it?

## - We need to open our 'blog/views.py'.

# So far 'post_list' view looks like this:
from django.shortcuts import render
def post_list(request):
    return render(request, 'monblog/post_list.html', {})
# Remember when we talked about including code written in different files?
# Now it's the moment when we have to include the model we have written
# in 'models.py'.We will add this line (in the second line) :
from .models import Post
# The dot before 'models' means "current directory" or "current application".
# Both 'views.py' and 'models.py' are in the same directory. This means we can
# use '.' and the name of the file (without '.py'). Then we import the name
# of the model ('Post').
# - But next, to take actual blog posts from 'Post' model we need 'QuerySet'.

## QUERYSET

# - So now we want published blog posts sorted by 'published_date', right?
# We already did that in 'QuerySets' chapter!
>>> Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
# Now we put this piece of code inside the 'blog/views.py' file by adding it
# to the function 'def post_list(request)':
from django.shortcuts import render
from django.utils import timezone
from .models import Post
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'monblog/post_list.html', {})

# - The last missing part is passing the 'posts' QuerySet to the template.
# (We will cover how to display it in a next chapter.)
# In the 'render' function, we already have parameter 'request' (so everything
# we receive from the user via the Internet) and a template file
# 'blog/post_list.html'. The last parameter, which looks like this '{}', is a place
# in which we can add some things for the template to use. We need to give them
# names. It should look like this:
{'posts': posts}
# Please note that the part before ':' is a string, you need to wrap it with quotes ''.

## THAT'S IT! Time to go back to our template and display this QuerySet.

# in your local console:
git add -A .
git status
git commit -m "Changed the monblog/views.py: dynamic data templates"
git push
# in the PythonAnywhere console:
git pull
# in the PythonAnywhere 'Web' tab: refresh with the "Reload" button.
# Refresh the 

## DJANGO TEMPLATES ############################################################

# Time to display some data! Django gives us some helpful built-in
# template tags for that.

## WHAT ARE TEMPLATE TAGS ?

# In HTML, you can't really write Python code, because browsers don't understand
# it. They only know HTML. We know that HTML is rather static, while Python
# is much more dynamic.
# Django template tags allow us to transfer Python-like things into HTML,
# so you can build dynamic websites faster and easier.

## DISPLAY POST LIST TEMPLATE

# In the previous chapter, we gave our template a list of posts in the 'posts'
# variable. Now we will display it in HTML.
# To print a variable in Django templates, we use double curly brackets with
# the variable's name inside, like this:
{{ posts }}

# Try this in your 'monblog/templates/monblog/post_lists.html' template.
# Replace everything from the second to the third <div> with {{ posts }}.
# Save the file and refresh the 'http://127.0.0.1:8000/' page to see the results.
# Now in the web page, all we've got is this:
Django Girls Blog
[<Post: Hello Third>, <Post: Hello Fourth>, <Post: Sampletitle>]
# This means that Django understands it as a list of objects.
# Remember from 'Introduction to Python' how we can display lists ? Yes, with
# 'for' loops! In a Django template, you do them like this:
{% for post in posts %}
    {{ post }}
{% endfor %}
# Try this in your template. Your webpage is now:
Django Girls Blog
Hello Third Hello Fourth Sampletitle
# It works but we want them to be displayed like the static posts we created
# earlier in the 'Introduction to HTML' chapter. You can mix HTML and template
# tags. Our body will look like this:
<body>
    <div>
        <h1><a href="">Django Girls blog</a></h1>
    </div>
    {% for post in posts %}
        <div>
            <p>published: {{ post.published_date }}</p>
            <h1><a href="">{{ post.title }}</a></h1>
            <p>{{ post.text|linebreaks }}</p>
        </div>
    {% endfor %}
</body>
# - Everything you put between {% for %} and {% endfor %} will be repeated for each
# object in the list. Now refresh your 'http://127.0.0.1:8000/' page.
# - Please note that we used a slightly different notation this time :
# {{ post.title }} or {{ post.text }}
# We are accessing data in each of the fields defined in our 'Post' model.
# Also the '|linebreaks' is piping the posts' text through a filter to convert
# line-breaks into paragraphs.

## ONE MORE THING

# It'd be good to see if your website will still be working on the public
# internet. Let's try deploying to PythonAnywhere again. 
# - in your local console:
git status
git add -A .
git status
git commit -m "Modified templates to display posts from database."
git push
# - in the PythonAnywhere console:
cd monblog
git pull
# - in the PythonAnywhere 'Web' tab: refresh with the "Reload" button.
# - Refresh the 'http://root35.pythonanywhere.com' page.

# If the blog posts on your PythonAnywhere site don't match the posts appearing
# on the blog hosted on your local server, that's OK. The databases on your local
# computer and PythonAnywhere don't sync with the rest of your files.

## Now go ahead and ty adding a new post in your Django admin:
http://root35.pythonanywhere.com/admin
# Then refresh your page to see if the post appears there.
# If it works, you can be proud ! You've earned a break !

## CSS MAKE IT PRETTY ##########################################################

# We don't want to start from scratch again. So once more, we'll use something
# that programmers released on the internet for free.

## LET'S USE BOOTSTRAP

# Bootstrap is one of the most popular HTML and CSS frameworks for developping
# beautiful websites : http://getbootstrap.com/
# It was written by programmers who worked for Twitter. Now it's developed
# by volunteers from all over the world.

# -- Install Bootstrap
# You only need to add this to your <head> in your 'monblog/templates/monblog/post_list.html':
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css">
# This doesn't add any files to your project. It just points to files that exist
# on the internet. Just go ahead and open your website and refresh the
# 'http://127.0.0.1:8000/' page. Looking nicer already!

## STATIC FILES IN DJANGO

# Finally we will take a closer look at these things we've been calling 'static files'.
# Static files are all your CSS and images. Their content doesn't depend on the request
# context and will be the same for every user.

# -- Where to put static files for Django
# Django already knows where to find the static files for the built-in "admin"
# app. Now we just need to add some static files for our own app, 'monblog'.
# We do that by creating a folder called 'static' inside the blog app (locally) :
mkdir monblog/static
# Django will automatically find any folders called "static" inside any of your
# apps' folders. Then, it will be able to use their contents as static files.

# -- Your first CSS file
# Let's create a CSS file now, to add your own style to your web page.
# Create a new directory called 'css' in your 'static' folder :
mkdir monblog/static/css
# Then create a new file called 'monblog.css' inside this 'css' directory :
echo " " > monblog/static/css/monblog.css
# and open it in your code editor. You'll only change the color of of your header:
# you can find the color codes for many colors at 'http://www.colorpicker.com/'
h1 a {
    color: #FCA205;
}

# Then we need to also tell your HTML template that we added some CSS.
# In the 'monblog/templates/monblog/post_list.html' file, add this line
# at the very beginning of it, in order to load the static files:
{% load staticfiles %}
# then in the <head> section, after the links to the Bootstrap CSS files, add
# this line:
<link rel="stylesheet" href="{% static 'css/monblog.css' %}">
# The browser reads the files in the order they're given, so we need to make
# sure this is in the right place. Otherwise, the code in our file may override
# code in Bootstrap files. We just told our template where our CSS file is located.

# Now your file should look like this:
{% load staticfiles %}
<html>
<head>
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css">
    <link rel="stylesheet" href="{% static 'css/monblog.css' %}">
    <title>Django Girls blog</title>
</head>

# Save the file and refresh the 'http://127.0.0.1:8000/' page.

## TEMPLATE EXTENDING ##########################################################

# Another nice thing Django has for you is template extending. It means that you
# can use the same parts of your HTML for different pages of your website.
# Templates help when you want to use the same information/layout in more than
# one place. You don't have to repeat yourself in every file! And if you want
# to change something, you don't have to do it in every template, just once!

## CREATE A BASE TEMPLATE

# - A base template is the most basic template that you extend on every page
# of your website. Create a 'base.html' file in 'monblog/templates/monblog'.
# - Then open it up and copy everything from 'post_list.html' to it.
# etc.
# - In the 'post_list.html' file, you'll connect these two templates together
# by adding an 'extends' tag to the beginning of the file:













PACKT PUBLISHING
*Expert Python Programming : best practices for designing, coding and distributing your Python software
*Mastering Python
Python Testing: Beginners guide
Python Testing Cookbook
*Python Object Oriented Programming
Learning Python Design Patterns
Mastering Python Design Patterns
Mastering Python Regular Expressions
Python High Performance Programming
*Learning Cython Programming

MySQL for Python

Getting Started with Python Data Analysis
*Learning Hadoop 2
Building Haddop Clusters
Big Data Forensics
*Deep Learning with Python
*Python Machine Learning
Python Machine Learning Cookbook
Mastering Python Machine Learning
Practical Machine Learning
Building Machine Learning Systems with Python
Python Machine Learning Blueprints
*Building Probabilistic Graphical Models with Python
**Mastering Probabilistic Graphical Models with Python
Building Interactive Graphs with ggplot2 and Shiny
Building Machine Learning Systems with Python
*Learning Data Mining with Python
Python Data Science Essentials
*Python Data Science Cookbook
**Mastering Python for Data Science
Clean Data – Data Science Strategies for Tackling Dirty Data
Mastering Python for Scientific Computing
Regression Analysis with Python
Matplotlib for Python Developpers
*Mastering Matplotlib
Learning Pandas
*Mastering Pandas
Learning SciPy for Numerical and Scientific Computing
Learning scikit-learn: Machine Learning in Python
Scikit-learn Cookbook
Mastering Machine Learning with scikit-learn
*Python Data Visualization Cookbook
**Mastering Python Data Visualisation
Building Responsive Data Visualizations with D3.js
Learning Predictive Analytics with Python

Web Development with Django Cookbook
Django by Example
Test-Driven development with Django
Tkinter GUI Application Development Blueprints

Python for Secret Agents
Python Game Programming by Example
Geospatial Development by Example with Python
Python Geospatial Development Essentials










################################################################################