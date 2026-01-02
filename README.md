## UPDATE

In order to save costs, all the AWS infrastructure has been terminated as of 2nd January 2026.The URL mentioned below: http://www.geography-quiz.net will not be accessible from this time onwards until I decide to resurrect this project.

## Geography Quiz

As you can see from the "Beginnings" section, this originally started out as a web-app equivalent of a desktop app I made using tkinter.

The features of the app are as follows:

The user opens the website, they have either the option to choose a difficulty or choose a continent. After the choice, a quiz is presented where one drags the "country" from the left and drops it over a "city" of choice on the right. The website is [here](http://www.geography-quiz.net/).

The source of data is two wikipedia pages. These are:
- https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Countries/Popular_pages
- https://en.wikipedia.org/wiki/List_of_national_capitals

This is the same from the desktop app. The idea is that you get a list of countries arranged in descending order of popularity and you join the table with the list of national capitals. In doing so, the data will have two features:

- It will have up to date data always
- By arranging in descending order of wikipedia page popularity, one could assume that the most popular countries had capitals which could easily be guessed and the countries with the least popular pages were harder to guess.

Due to my familiarity with Python, and having dabbled with Flask in the past, and having had some experience with PHP and JavaScript - both Vanilla and React, most of the functionality did not give me trouble.

For me, the most enjoyable and challenging part was getting it to work on Elastic Beanstalk on AWS. This meant I had to set up a CI/CD pipeline using Github actions, create a procfile, use my aws secret and access key and use the aws cli for eb. (I recommend using WSL for this if you're on windows)

During this phase, the most interesting aspect was setting up RDS for Postgres on Elastic Beanstalk. Locally I had used SQLite and mostly performed direct SQL Queries. To make Postgres work on Elastic Beanstalk and also make SQLite work locally, I had to use SQLAlchemy which was pretty cool to learn. I will probably start applying it more widely at work and in projects.

During this phase, I had to figure out how to refresh the data. Locally, this was a solved problem - just use SQLite. There is a hyperlink called "Refresh Database" and if run locally, it downloads the data from the two wikipedia pages mentioned above.

But with RDS + Postgres this is not advisable because it is slow, may result in bans for excessive scraping and just common sense goes against it. So I used AWS Lambda function triggered by EventBridge every week.

The function itself was trivial to write, but I had great difficulty getting psycopg2-binary to work. The only solution that worked was [this one](https://github.com/keithrozario/Klayers/issues/392#issuecomment-2954706640). I used this arn as a layer and it worked.

There may be some front end polishing that I would like to add in the future. But I am rather pleased with how this turned out.

# Beginnings.
To start with, this  will be the web equivalent of the [Country vs Capital](https://github.com/shannu1995/Country-Vs-Capital)) project.

But it will be nice to expand upon it with other geography-themed types of quizzes.
