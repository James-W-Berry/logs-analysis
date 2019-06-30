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
$ cd VM/vagrant
$ vagrant up
$ vagrant ssh
```
After connecting to the Vagrant VM, the PostgreSQL database server will already be starting. Use the psql command line tool to populate the database with the [provided data](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).
```sh
$ cd vagrant
$ psql -d news -f newsdata.sql
```
Next, use the psql tool to connect to the news database and create the following database views.
```sh
$ psql news

news=> create view popular_articles as
news=> select count(*) as num, path
news=> from log
news=> where path like '/article/%'
news=> group by path
news=> order by num desc
news=> limit 3;

news=> create view article_popularity as
news=> select count(*) as num, path
news=> from log
news=> where path like '/article/%'
news=> group by path
news=> order by num desc;


news=> create view error_requests as
news=> select date(time) as date, count(*) as error_requests
news=> from log
news=> where status not like '2%'
news=> group by date(time)
news=> order by date;

news=> create view all_requests as
news=> select date(time) as date, count(*) as all_requests
news=> from log
news=> group by date(time)
news=> order by date;
```

Once the views are created, run the log analysis tool and verify the contents of *program-output.txt*.
```sh
$ python logs-analysis.py
$ cat program-output.txt
```