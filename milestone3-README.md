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

### Why did you choose to test the code that you did?

I chose to test the code that I did so that I could test and verify that most of the lines were doing what they were supposed to be doing and were consistent in that respect. I tested most of the bot code using unmocked tests because the code simply checked whether the parameters (strings) passed matched a test string. If they matched, it would proceed to run certain commands until it returned a response string. Testing this ensured that the bot was checking the correct parameters and responding appropriately. I also checked cases where the parameters passed did not match any of the test strings, in which case I checked that the expected and actual return strings did not match using `AssertNotEqual`. I also tested the server code in app.py to ensure that the logic between socket functions/commands and database functions/commands were sound. I checked if certain socket calls updated variables like the user count or request sid. These tests made sure that different functions were completing their specific tasks and sending the correct data to the correct endpoints. Essentially, the overall purpose of testing the code via unit testing is to cover all the lines of code, or in this project at least 90% so that all bases are covered. Also, as the app becomes more and more complex, we don't want to rely on our old testing methods of running the app and seeing if all functionalities work properly. With a complex app, this method of testing is inefficient because you would have to test a lot of functionalities every time you update it. With unit testing, when you update the code, the past tests can run quickly and still apply. All that is needed is to create tests for the updated code so that all of the lines are covered. (Make tests as you update the code.)

### Is there anything else you would like to test if you had the time (or was asked to do so)?

If given more time or asked to do so, I would test more of the front-end portions of the app. For this milestone, I did linting, but it was moreso to clean up the code itself and not the output. With linting, the code styling like indentation, format, etc. were tested and organized, but I would focus on making sure that the front-end code makes the app look like what I intended for it to look like. I think testing the javascript will ensure that the user interface is stable, consistent, and intended. I want to make sure that nothing breaks or becomes blank or gives errors because they are ultimately what the users will see. I would also want to test the database portions of the app as well as the sockets. These were not really "tested" since they were mocked for this project. The purpose was to make sure that the logic of the server code was correct and the big picture tasks were completed. I'm not quite sure how I would test the db and socket portions, but I feel like they are important since they are the base for the app's functionality. If these areas were to fail, then there is no chat app. One failure can result to the entire app crashing, which is a cause for concern. Testing these will ensure that the app's functionality is consistent and dependable. It will also help lessen testing complications when more functionalities are added to the app.
