# Sporty.com Web App
Sporty is a web application where users can find and register for recreational local sport clubs. Users can create posts, bookmarked their favourite blogs. 

## Goal of the Project:
The goal of this project was to build a full stack web application using Flask. My passion for sports led me into designing and building this project. Sporty.com was built with a soccer game in mind. Players/prospects looking for a team can view details of available teams an click to register; or Will want to post something interesting about sports in terms of mini-blog. Other players can bookmark the blog if they're interest in it. 

# Lesson Learnt

To bring this project to a completion I applied a variety of technical and non-technical skills set. Having a specialization in Business Information Systems managament, I was able to apply System thinking and design principles; I managed to think how different entities can or will interact with this web application. For example How Users can register for teams; What's relationship between the two entities; What are the constraints. 

Lastly, I successfully implement different routes and logic on how to handle different Post requests methos. For example, Using Javascript; I used addEventListers to change the color of blogs where use had already bookmarked and using python I handled the the double counting of the bookmarked Blog. Each Blog has counts on how many times have been bookmarked by a user. Once a user clicks the blog, the data will be sent to the server and the Bookmark table will be updated according. Now, if a user clicks again same post; The program checks if the current user  have already liked the current post. This is done through query the database and validate it before updating the count. 

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


### Now tproject set up is ready; 'CD to sport directory and run the following commands in your terminal.
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

