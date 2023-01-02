# emotional_diary v0.1.0-alpha

## Video demo: https://youtu.be/dOVb-wrIo10

## Description
  A web app builded using Flask, in which you can pair emotions with colors and have a daily register of which emotions dominated your day. This is my CS50x final project and my first project of this scope! Any comments/suggestions are welcome. Code design based on CS50 finance and Flask tutorial https://flask.palletsprojects.com/en/2.2.x/tutorial/

## Structure
This project contains the following directories and files
- README.mb
- main.py
- .gitignore
- diary (directory)
  - \__init__.py
  - auth.py
  - views.py
  - db.py
  - helpers.py
  - requirements.txt
  - schema.sql
  - static (directory)
    - style.css
  - templates (directory)
    - layout.html
    - home.html
    - manage_emotions.html
    - change_password.html
    - error.html
    - login.html
    - recover.html
    - recover_2.html
    - register.html

## Contents
In this section the contents of each file are briefly described.

#### README.md
**This** file contains the documentation of the project.

#### main.py
Creates an instance of the app ensuring it is created from and only from there. Sets debug mode on and the port for the server at 5001 by default.

#### .gitignore
Sets which files and directories are ignored by git, edit at your convinience. The most importnat are the directories **flask_session** and **instance**. The last one contains the local database. 

### diary (directory)
This directory contains all the files related to the app.

#### \__init__.py
Defines the **create_app** function which is used to initialize the flask app in **main.py**. Defines the constants **SECRET_KEY**, **DATABASE** and **TEMPLATES_AUTO_RELOAD**. The first should be changed for security if the app should be deployed, and the second indicates the **instance** directory location to the app, so it can access the database. Also, it ensures the existence of the **instance** directory by creating it if it does not exists already. Next, the function imports **db.py** so it can initialize the database using **init_db** and close the conecttion stablished using **init_app**. Finally it registers the blueprints of the app and sets the url prefix **/auth/** for all routes contained in **auth.py** and */* for all contained in **views.py**. Returns a **Flask** object.

#### auth.py
Contains all the logic related to registration and authentification. 
The routes inside are:
- login: Deals with user authentication using the user's password hash. 
- logout: Deals with closing user session by clearing the **session** object.
- register: Deals with signing in the users setting their name, password and security phrase.
- change_password: Allows user to change their password after login. It requires authenthication to prevent malicious changes.
- recover: Deals with the authentication of the user using their security phrase. Redirect user to change their passwords after successful auth.
- recover_2: Updates an user password after successfully authentication using security phrase.
- load_logged_in_user: Loads user id into **session** object and made it available to all views using the **g** object.

#### views.py
Here is implemented the logic allowing the user to update their emotion-color pairs and to assign them to the current day. The routes cotained here are:
- index: Allows the user to add to the current day a emotion-color pair. It renders automatically an updated template with each addtition.
- manage_emotions: Adds emotion-color pairs to the data base and shows them in a table to the user.
- delete_emotions: Allows the user to delete any given pair.

#### db.py
Contains the logic needed to connect and operate the data base. Taken from the Flask tutorial (check file for link) since it is a component so basic that it would have been implemented in an almost identical manner regardless the source used.

The functions inside are:
- get_db: Check if there is a connection to the database and if not initilize one and adds its cursor to the **g** object. Sets the response to the sql queries as **row** objects, so columns can be access by name. Returns the cursor object inside **g**.
- close_db: Deletes the cursor from **g** and close the conection to the database.
- init_db: Stablish a connection to database and executes the script in **schema.sql** to create the database file in **instance** directory.
- init_app: closes database connection when initializing the app.

#### helpers.py
This file contains one helper function **apology** which allows to display the **error.html** template with customized error messages and error status codes. Also the **login_required** decorator is defined here allowing to show some views conditionally.

#### requirements.txt
Libraries needed by the project.

#### schema.sql
This file contains the schema of the database **diary.db**. It contains the following tables:
- users: Main table, contains usernames and passwords and phrases hashes.
- settings: Here the emotion-color pairs are stored and linked to a single user.
- register: This table saves the emotion-color pair assigned to a day per user.
The script will delete any existent tables with those names before creating them.

### static (directory)
This file contains the css (and hopefully in the future js) related to the app.

#### style.css
Contains one style class applied to the table at the template **home.html**.

### templates (directory)
All html templates are contained here. Every template is asociated with the route of the same name (unless specified other way) except **layout.html** which is the base template.

#### layout.html
Base template implementing the navigation bar and the buttons **Login**, **Logout**, **Register** and **Settings**. The buttons are displayed conditionally depending if the user is logged or not. It contains 2 Jinjas blocks, **title** and **main**, that are expanded in the other templates.

#### home.html
Implements a table that is dynamically expanded using Jinjas conatining the columns **date** and **emotion**. The **emotion** cells contain the emotion in text and its background color is the one defined by the user. Associated with the **index** route in **views.py**.

#### manage_emotions.html
Implements a 2 field form where the user can input an emotion and a color (in python style hex). The button provided adds the color to the table (expanded using Jinjas). The emotion-color pairs are displayed as in **home.html**. Also implements a button in each row to delete it. Associated with **manage_emotions** route and **delete_emotion** route.

#### change_password.html
Implements 3 field form: first for user authenticathion using password, second and third for new password regitration.

#### error.html
Displays cutomize error code and message using Jinjas. It is managed by the function *apology*. 

#### login.html
Contains 2 fields form for user authentication.

#### recover.html
Contains a 2 field form for user authentication using the security phrase.

#### recover_2.html
Implements a 2 field form for new password registration.

#### register.html
Implements a 4 field form for new user registration.

## Design discussion
This section is devoted to explain the ideas behind the deign of this project, and to check alternatives/improvements to the current implementation.

The base concept of this project was the idea of an emotional diary. The current implementation though functional is rought. Some design desitions tha could be improved are:

- All interactivity is provided by requests to back-end hich would not escalate well as it needs ot recharge the whole page each time. All interativity in the **home.html** and **manage_emotions.html** templates should be re-implemented using ajax, so latency between action -i.e. adding an emotion-color pair- and update could be minimized. 
- Change to a kinder color palette.
- The visual design of **home.html** and **manage_emotions.html** can be improved to better reflect the app's base concept.
