#!/usr/bin/env python
import psycopg2
import datetime

DBNAME = "news"


def get_popular_articles():
    db = psycopg2.connect(dbname=DBNAME)
    c = db.cursor()
    c.execute(
        """
            select title, num
                from articles, popular_articles
                where popular_articles.path like '%' || articles.slug || '%'
                order by popular_articles.num desc;
        """
    )
    result = c.fetchall()
    output_file = open("program-output.txt", "a+")
    output_file.write('Most popular articles:\r\n')
    for row in result:
        output_file.write('"%s" - %s views\r\n' % (row[0],  row[1]))
    output_file.close()
    db.close()


def get_popular_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        """
            select sum(num) as total_views, name
                from authors,
                (select num, author
                    from article_popularity, articles
                    where path like '/article/' || slug
                ) as views

                where author = authors.id
                group by name
                order by total_views desc;
        """
    )
    result = c.fetchall()
    output_file = open("program-output.txt", "a+")
    output_file.write('\r\nMost popular authors:\r\n')
    for row in result:
        output_file.write('%s - %s views\r\n' % (row[1],  row[0]))
    output_file.close()
    db.close()


def get_error_days():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(
        """
            select error_requests.date, cast(error_requests as float) /
            cast(all_requests as float) * 100 as error_percent
                from error_requests, all_requests
                where error_requests.date = all_requests.date
                and cast(error_requests as float) /
                    cast(all_requests as float) * 100 > 1;
        """
    )
    result = c.fetchall()
    output_file = open("program-output.txt", "a+")
    output_file.write('\r\nDays with more than 1% HTTP request errors:\r\n')
    for row in result:
        error_date = datetime.datetime.strptime(str(row[0]), '%Y-%m-%d') \
            .strftime('%B %d, %Y')
        output_file.write('%s - %0.1f%% errors\r\n'
                          % (error_date,  row[1]))
    output_file.close()
    db.close()


output_file = open("program-output.txt", "w").close()
get_popular_articles()
get_popular_authors()
get_error_days()
