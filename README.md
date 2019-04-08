# udacity_fullstack_project4

## **PROJECT**
 This project creates a cataloging app. Using a python-flask based back end and SQLAlchemy to parse a database and dispatch custom html as needed for the user requests.There is some prepopulated items in the database upon launch, that can be viewed by any user. These items are arranged into 5 categories and can be viewed either by category or a list of the most recent items. Using a google oauth sign in users can login and gain the ability to add items. the site features a permission system and allows users to edit or delete items. but only ones they have created. The application also exposes a json endpoint that displays all items inside their respective categories

## **DEPENDENCIES**
* Python 2.7
* flask, sqlalchemy, and oauth2client libraries
* an internet connection

## **SETUP/INSTALLATION & USAGE**
* To Setup: follow guidelines provided in the udacity vagrant vm setup. vagrant can be found here https://www.vagrantup.com/downloads.html, the vagrant box files can be downloaded here https://github.com/udacity/fullstack-nanodegree-vm. Extract the vagrant box to any directory you have access two and navigate to it. Then open a terminal instance at this directory and input the command "vagrant up" to initialize and launch your virtual machine (this may take some time on first run as it is gathering a lot of information). After the vm has been intiallized use "vagrant ssh" in your terminal to enter into the vagrant vm. Then load all files in this repo  into the shared folder of a vagrant instance's shared folder directory (/vagrant under the vm's extracted location on the host machine). All dependencies should be present on this machine already

* To Run: in your vagrant vm "cd <path-to-where-you-input-the-files>" and initialize the database's items, categories, and the inital user by running "python createDB.py". Once that has finished execution run the app with "python server.py", and navigate to http://localhost:8000/ to lod the index page. to access the json endpoint navigate to http://localhost:8000/catalog.json.


### **NOTES/KNOWN BUGS**
* There is a known bug where the index page may not display the add item's button without a page refressh or navigation. likewise the add item's button may not disappear until  a page navigation or refresh, however a logged out user will not be able to gain access to add items regardless of the button's presence.
* only localhost is operation if you want to use google oauth as straight ip addresses do not work for oauth. do not use 127.0.0.1 if you want to sue all the features of this site
* there were some minor changes needed to deal with google plus shutting down earlier this year, consider updating code to ccomodate
* the default dbsession managemant from the instructor code isn't thread safe, consider updating the code to use scoped sessions like this code, or utilizing the flask-sqlalchemy libaray to avoid this kind of threading issue

