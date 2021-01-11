# Urbvan Test Microservice
API Rest Microservice - Urbvan postulation Test

This README sets the use of this application to deploy the microservice API Rest.

### What is this application for? ###

* Management of Van vehicle data on a database.
  Search, Create, Update and Delete Van data on database. 
* Version: v.1.1.A10.5
* [API Microservice Documentation](https://urbvan-microservice-test.herokuapp.com/)

### How do I get set up/deploy it? ###

1.- Go to the GitHub remote repository: [GitHub remote microservice repository](https://github.com/jorgeMorfinezM/urbvan_test_microservice) and validate the 
steps of this Readme deployment documentation/API code and general data.

2.- On your CLI (Command Line Interface) tool, clone the remote repository from the 1st step using the version control 
systemGit command on your local path repository/directory. 

3.- Verify all code/data from GitHub remote repository are on the local repo.

4.- Copy all API code to a new local path/directory, only to deploy the application you need: `auth_controller`, 
`constants`, `db_controller`, `logger_controller`, `logs`, `model`, `static`, `templates` directories and then, copy 
the `__init__.py`, `app.py`, `Procfile`, `requirements.txt`, `wsgi.py` files. 

5.- Set on the new path directory established on 4 step. 

6.- Install the Heroku CLI Platform as a Service [following the instructions](https://devcenter.heroku.com/articles/heroku-cli)
 depending of your operating system. 
 
7.- If you do not have an Heroku account, [Create your own](https://signup.heroku.com/)

8.- Once that is out of the way, on the Heroku web console dashboard, select New -> Create new app.
Once the application is created on Heroku, we're ready to deploy it online.
   
9.- Execute on your command line tool in your new path app the `git init .` command to initialize the local repository.   

10.- Execute on your command line tool the `git add -A` command to add the app code to the local Git repository.

11.- Execute on your command line tool the `git commit -m "message_to_this_commit"` command to commit the changes on 
code to the local Git repository.

12.- If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key. 
Then, execute the `heroku login -i` command and set your username and password registered on the dashboard.

13.- Execute the `heroku login` command on your command line tool.

14.- Execute the `heroku git:remote -a {your-project-name}` command replacing `{your-project-name}` to your 
Heroku and repository name.

15.- Execute the `git push heroku master` command.  

16.- Testing the API. In the log that has been shown in the console you will find a link for your [application](https://{your-project-name}.herokuapp.com/), 
this link can also be found under the Settings tab, in the Domains and certificates section Heroku console web dashboard.

17.- If you wanna change the API code, make the change need to execute the 10 to 15 steps. 

18.- If you wanna verify the LOG of the API, execute `heroku logs --tail` command.
 
### Where do I find the documentation for the App? ###

* [Repo owner or admin](mailto:jorge.morfinez.m@gmail.com) 
* [Repository Workspace](https://github.com/jorgeMorfinezM/urbvan_test_microservice)
* [API Use Documentation](https://urbvan-microservice-test.herokuapp.com/)
* [API Design Documentation](shorturl.at/nsMSX)
