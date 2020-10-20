# CS 490 Chat App

### This is a real-time chat/messaging app that uses React, Flask, Socket.io, PostgreSQL, and SQLAlchemy.
### It features a chat bot with multiple functionalities, including fun translations using the Fun Translations API and random joke using the Joke API.

## React Set Up:

1. Clone this repository in your terminal: `git clone https://github.com/NJIT-CS490/project2-m1-gda6` and `cd` into it.
2. Install flask:
  * `sudo pip install flask` or `sudo pip3 install flask` or `pip3 install flask`
3. Install python-dotenv:
  * `sudo pip install python-dotenv` or `sudo pip3 install python-dotenv` or `pip3 install python-dotenv`
4. Install the following: <br>
  _Note: If you encounter error messages, use `sudo` then one of the commands below._ <br>
  _Note: If "pip cannot be found", do `which pip` then `sudo [path to pip from which pip] install` then the corresponding package below._
  
  * `npm install`
  * `pip install flask-socketio`
  * `pip install eventlet`
  * `npm install -g webpack`
  * `npm install -save-dev webpack`
  * `npm install socket.io-client --save`
  * `npm install react-google-login`
  
## PSQL and Python Prep:

1. Update yum: `sudo yum update`. Enter **yes** to all prompts.
2. Upgrade pip: `sudo [path to pip from which pip] install --upgrade pip`
3. Get psycopg: `sudo [path to pip from which pip] install psycopg2-binary`
4. Get SQLALchemy: `sudo [path to pip from which pip] install Flask-SQLAlchemy==2.1`

## PSQL Setup:

1. Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-develpostgresql-contrib postgresql-docs`. Enter **yes** to all prompts.
2. Initialize PSQL database: `sudo service postgresql initdb`
3. Start PSQL: `sudo service postgresql start`
4. Make a new superuser: `sudo -u postgres createuser --superuser $USER` <br>
   _Note: if you encounter an error "could not change directory", that's fine. Go to the next step_
5. Make a new database: `sudo -u postgres createdb $USER` <br>
   _Note: if you encounter an error "could not change directory", that's fine. Go to the next step_
6. Confirm your user was created:
    * `psql`
    * `\du`. Confirm ec2-user shows up as a user.
    * `\l`. Confirm ec2-user shows up as a database.
7. Create a new user:
    * `psql` if you exited psql from previous step.
    * `create user [username] superuser password '[password]';` <br>
    _Note: `[username]` is your created username and `[password]` is your created password._
    * `\q` to quit psql
8. Make sure you are in `project2-m1-gda6`. Create a new file `sql.env`. Add `SQL_USER=[username]`, `SQL_PASSWORD=[password]`, and `DATABASE_URL=postgresql://[username]:[password]@localhost/postgres` to the .env file. <br>
    _Note: `[username]` is your created username and `[password]` is your created password from step 7._
    
## Run App

1. Run `sudo service postgresql restart`
2. Make sure that the items in `sql.env` match your credentials from "PSQL Setup step 7".
3. Run the code: `python app.py`
4. If on Cloud9, click **Preview** and **Preview Running Application**. <br>
   _Note: You may need to do a hard refresh to properly view the app page._

---

## Deploy App Using Heroku

1. Sign up for heroku at (https://signup.heroku.com/login)
2. Install Heroku: `npm install -g heroku`
3. Make sure that your local copy of the repository is up to date: `git status`. If not, `git add [files]` and `git commit -m "[message]"`. <div>
   _Note: `[files]` are the files listed from git status and `[message]` is a description of the changes made._
4. Log in to Heroku in your terminal: `heroku login -i` and enter your credentials.
5. Create app: `heroku create`. Remember the link given for your app.
6. Create db: `heroku addons:create heroku-postgresql:hobby-dev` and `heroku pg:wait`
7. Make yourself the owner of db: 
    * `psql`
    * `ALTER DATABASE Postgres OWNER TO [username];` <br>
    _Note: `[username]` is your created user name from "PSQL Setup step 7".`_
    * `\l` and make confirm that the db name **postgres** is owned by your `[username]`.
8. `heroku pg:push postgres DATABASE_URL` and enter Heroku credentials when needed. <br>
    _Note: if you encounter "Warning: errors ignored on restore: 2" and "pg_restore errored with 1", that's fine. Go to the next step._
9. Determine what tables you have:
    * `heroku pg:psql`
    * `select * from chat` and ensure that the table displayed is the one used in **"Run App"** step. 
    * Exit using CTRL-D
10. Make sure that your local copy of the repository is up to date: `git status`. If not, see step 3.
11. Do `git remote -v` and ensure that your heroku app link has "fetch" and "push" properties.
12. Push to Heroku: `git push heroku main` or `git push heroku master`
13. Go to your heroku link from step 5. It should display the chat app. <br>
    _Note: If there is an application error even after a hard refresh, go to the app page on the Heroku site, click **More**, **Restart all dynos**, and the red **Restart all dynos** button._

---

## Issues Encountered:

1. I was having trouble finding a way to determine the number of users that were connected to the server and using the app. 
   I figured that this task should be done in the socketio connect and disconnect portions of the server side. 
   After searching online for a possible solution, I came across (https://github.com/miguelgrinberg/Flask-SocketIO/issues/580). 
   This method was similar to my inital thinking and plan, so I decided to implement it in my app. 
   Essentially, every time there is a connect, a global variable increases by 1 and is then emitted to all channels. 
   Similarly, every time there is a disconnect, the global variable decreases by 1 and is emitted to all channels. 
   This was a simple way of doing the task, but it works reliably and well.
   
2. I had some difficulty trying to retrieve the usernames or ids of the users or clients. 
   I was thinking that I could have a login portion where the user could input their desired username, which would be displayed in the chat. 
   After going through Slack, I learned that I could simply use the client ids and use this to identify each user. 
   Whenever the server received a new message, I simply did a `request.sid` and combined it with `data["message"]`. 
   This string was then added to the db and emitted to all channels or clients.
   Essentially, the user id of the person who sent the message was combined with the actual message in the server side and then emitted to all. 
   
3. After trying to `npm run watch` and `install webpack-cli`, I got an "Error: cannot find module 'webpack-cli'" and "npm ERR! code ELIFECYCLE errno1". 
   I tried an online suggestion to install "webpack-cli" globally by doing `npm link webpack-cli`. 
   Doing this gave me another error: "Invalid configuration object" since my webpack was "not initialized using a configuration obj that does not match the API schema". 
   After copying and pasting the error, I found something on github (https://github.com/laravel/framework/issues/26238). 
   It had multiple steps: `npm cache clean --force`, which produced in the terminal: "I hope you know what you are doing". This really had me sweating.
   Then, `rm -rf node_modules`, `npm install`, `npm run dev`, `npm run watch`. 
   This procedure worked and was able to get my app running. 
   
4. When I changed the variables in models.py and app.py that related to the database, I got sqlAlchemy errors. 
   I figured that making these changes also changed the table that the app was using. 
   Since there was no table with the new name, then the .py files were not using any.
   I thought that I should create a new db/table to match the changes. 
   I watched "Lect 11 Demo 2" and learned how to check different users and view table. 
   I went on Slack and read previous posts and learned how to change user roles. 
   Then, on Discord, someone posted the powerpoint slide that explained how to create models in postgresql: `python`, `import models`, `models.db.create_all()` 
   I used all of these resources to create a new table that reflected the new name from the .py files. 
   This worked and helped my app run properly.
   
5. When I followed the steps from "Lect 11 Demo 3", I got to the point where I had to change `DATABASE_URL = postgresql://...`.
   After doing this and updating `sql.env` to reflect the changes, I got "SqlAlchemy_exc.OperationalError could not connect to server. Connection refused".
   Since the demo said that the app should still work even after changing and removing the specific variables, I could not get mine to after doing the same changes.
   I ended up just googling the error to find a solution. What worked was doing `sudo service postgresql start` before doing `python app.py`
   I thought I no longer had to run that command after the changes, but I noticed that I no longer had to do `npm run watch`.
   Now, doing `python app.py` by itself works to run the app, which I thought was an indication that I was doing things correctly.
   
   
## Improvements:

1. One thing I would really want to improve is how I retrieve and create the username for each client or user.
   What I have right now is functional since it identifies the source of each message and demonstrates that each one comes from a different user.
   However, the actual "user name" that is displayed is the client id, which is just very long line of numbers and letters.
   This makes the message/chat box appear sloppy since the username alone takes almost half the screen.
   To improve this, I would have the user input a username that they would want to use. 
   This would require a separate input field and when the user submits, this name would be sent to the server using sockets.
   The name would be stored in another field or column of the db/table. However, I'm still unsure how I would retrieve the correct username per corresponding message.
   Right now, I'm thinking of connecting the chosen username to the client.sid and matching it with the client.sid that is sent to the server every time a specific user sends a message.
   When a user sends a message, it would arrive to the server and be connected to the request.id. The request.id would be connected to the user name, which is stored in the db table.
   
2. A feature I would want to have is an authorization or login step before getting access to the chat app. 
   This was actually discussed during lecture using the Facebook OAuth tool or process.
   I would not reinvent the wheel and create my own OAuth process.
   Instead, I would use an external source's like Facebook or Google and connect it with the app so that their OAuth would manage logins to my app.
   This makes it so that my system is more secure and it's simply way easier than doing it from scratch.
   As mentioned in (1), the username could be retrieved during login and be used for identification in the actual chat box. 
   This would also contribute to the app's aesthetic and organization since it will make it look cleaner.
   
3. Another feature I'd want to have in the app is the ability for the user to create separate rooms.
   Right now, the chat app consists of only one 'global' server where everyone is communicating.
   This is not really ideal, especially when more people log in and use the app. It'll get too cluttered and full, minimizing the ability for effective and efficient communication.
   This feature is probably the one that I know the least on how to achieve. Right now, I think it would have to do something about the sockets.
   Though, all the users connect to one server, so I'm not sure how it would be done unless multiple servers are used?
   There may be an external API that can be used to create multiple rooms, but I'm not sure what it may be or if it is even necessary.
   I may need to create separate jsx Content files, which represents as each separate room?
   
4. One aspect of the chat app right now that I think does not look the best is that all the messages appear on the left side of the text box.
   Usually, the standard is to have your own messages on the right and everyone else's on the left.
   Right now, since I'm emitting all messages from one database, I could not differentiate between individual messages and determine which ones should be on what side.
   One possible solution is to have separate fields or columns for the messages, depending on the client.sid they are associated with. 
   However, with this, I'm not sure how I can display chat history in sequential order.
   When I emit all messages from one db, I can maybe check their client.sid and if it is a certain one, depending on the corresponding client end, it would be on the right side, if not it should display on the left. I'm honestly not sure, but these are the things I would want to incorporate and implement in this chat app.
