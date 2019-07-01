Logs Analytics
=============
Dependencies
+ [Python 2](https://www.python.org/downloads/release/python-2712/)
+ [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
+ [Vagrant](https://www.vagrantup.com/downloads.html)
+ [News data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)


## Project Setup
Start the Vagrant image and connect
```sh
cd VM/vagrant
vagrant up
vagrant ssh
```
After connecting to the Vagrant VM, the PostgreSQL database server will already be starting. Use the psql command line tool to populate the database with the [provided data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).
```sh
cd vagrant
psql -d news -f newsdata.sql
```
Next, use the psql tool to connect to the news database and create the following database views.
```sh
psql news

create view popular_articles as
select count(*) as num, path
from log
where path like '/article/%'
group by path
order by num desc
limit 3;

create view article_popularity as
select count(*) as num, path
from log
where path like '/article/%'
group by path
order by num desc;

create view error_requests as
select date(time) as date, count(*) as error_requests
from log
where status not like '2%'
group by date(time)
order by date;

create view all_requests as
select date(time) as date, count(*) as all_requests
from log
group by date(time)
order by date;
```

Once the views are created, run the log analysis tool and verify the contents of *program-output.txt*.
```sh
python logs-analysis.py
cat program-output.txt
```

## Program Design
The Logs Analysis project answers three key questions about the online news website.
<br/>
<br/>

**Goal 1: Find the three most popular articles recorded in the database.**

Strategy: First, find the most accessed articles from the log table using the generated popular_articles view. Second, find the article title from the articles table. Finally, construct a well-formatted output to populate *program-output.txt*.
<br/>
<br/>

**Goal 2: Find the three most popular authors recorded in the database.**

Strategy: First, get a ranking of all articles from the log table using the generated article_popularity view. Second, find each articles author id from the articles table by comparing the path and slug. Third, add up each author's total from their id. Finally, construct a well-formatted output to populate *program-output.txt*.
<br/>
<br/>

**Goal 3: Find the days where >1% of requests resulted in errors.**

Strategy: First, get all the requests and the requests generating a non-200 HTTP code each day using the all_requests and error_requests views. Second, calculate the error percentage for the whole day and return the days where the percentage is over 1%. Finally, construct a well-formatted output to populate *program-output.txt*.