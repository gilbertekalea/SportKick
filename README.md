# SportKick
Sporty is a web application where users can find and register for recreational local sport clubs. Users can create posts, bookmarked their favourite blogs. 

## Goal of the Project:
The goal of this project was to build a full stack web application using Flask. My passion for sports led me into designing and building this project. Sporty.com was built with a soccer game in mind. Players/prospects looking for a team can view details of available teams an click to register; or Will want to post something interesting about sports in terms of mini-blog. Other players can bookmark the blog if they're interest in it. 



# Project Features
        User authentication using Flask_login
        Bookmarking/Favourite
        Account creation/login
        Information Access restriction -> Some features/pages can only be accessed by users who have created account and they're logged in.
        Customized Dashboard for User profile data ->Blogs created, Blogs bookmarked, Team registered, 
        Email automation -> When a user registers for sport, or creates account, or just general emails etc. 

# Non Technical Skills 
I applied what I learnt from my undergraduate program on system design and modeling to provide the most minimal and yet easy to understand flow chart and entity relational diagrams to average person. 

#### [Database Entity Relational Diagram IMAGE BELOW](https://lucid.app/lucidchart/b89e6222-ec44-4925-8b19-a9ce1d67381c/edit?viewport_loc=0%2C48%2C2274%2C1074%2C0_0&invitationId=inv_7b379fb1-088d-465f-a412-92f7c02b9b80)

#### [Website flow diagram/Flow chart](https://lucid.app/lucidchart/b89e6222-ec44-4925-8b19-a9ce1d67381c/edit?invitationId=inv_7b379fb1-088d-465f-a412-92f7c02b9b80)

# Technical skills:
        Python Object Oriented Programming - utilized the use of classess, and functions; 
        Web Development technologies and libraries --> Used primary boostrap to design the layout of this project. Also, used Javascript to implement eventlisters. 
        I used Jquery ajax to implement Assynchronous programming since flask reloads the page when POST request is made.   
        Sqlalchemy -> Object relational Mappers.

### How to run this project on your machine. 
### First thing first: You need to install flask and other dependencies. run the following command; 
        windows:
        pip install -r requirements.txt


### Now project set up is ready; 'CD to sport directory and run the following commands in your terminal.
    Powershell:
        $env: FLASK_APP = "run.py"
        $env: FLASK_ENV = "development"
        flask run

    Command prompt:
        set FLASK_APP=hello
        flask run

    Bash:
        export FLASK_APP=hello
        flask run

    Fish:
        set -x FLASK_APP hello
        flask run

### After executing the above command; You will see link that looks this click on it and view the application on the browser:
        Running on http://127.0.0.1:5000/

