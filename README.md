## Wage Comparison Project

This repo stores the code to run and analyze our experiment on wage comparisons.

The `app` folder contains all code needed to run the experiment using oTree.

To install numpy, type 'pip3 install numpy' on your terminal.

### Running on Heroku

App was set up to run on Heroku by following [these directions](http://otree.readthedocs.io/en/latest/server/heroku.html?highlight=heroku).

Important note: since the actual web app is in a subdirectory of the git repo, pushing the app to Heroku must be done with a slightly modified command. Instead of 

	git push heroku master

you must run

	git subtree push --prefix app heroku master

(See [this post](https://coderwall.com/p/ssxp5q/heroku-deployment-without-the-app-being-at-the-repo-root-in-a-subfolder) for details.)  The above command should be run every time you want to update the heroku app. Note that the app does *not* update automatically if you push to github.  You should also run

	heroku run otree resetdb

if you have added/removed a field in `models.py`.  In general, any otree command can also be run remotely on heroku with 

	heroku run otree <command>

though `resetdb` is the only one you should need.  You do *not* need to run `runserver`, as this is done automatically when you push to heroku.

