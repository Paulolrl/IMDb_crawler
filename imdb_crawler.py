#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from lxml.html import fromstring
import codecs
import sys
import csv
import unicodecsv as csv


def extractmedia(movie):
  return (movie['imdb'] + movie['metascore'])/2


goodmovies = []
titles = set()
analised = 1
genres = []
args_size = len(sys.argv)

for i in range(1, args_size - 3):
    genres.append(sys.argv[i])

genres = genres if len(genres) > 0 else ['action', 'comedy', 'mistery', 'fantasy', 'thriller', 'drama', 'sci-fi', 'sport']

min_year = int(sys.argv[args_size - 3])
min_media = int(sys.argv[args_size - 2]) * 20
pages_per_cat = int(sys.argv[args_size - 1])


for genre in genres:
    for numpage in range(1, pages_per_cat * 50, 50):
        page = urllib2.urlopen('https://www.imdb.com/search/title/?title_type=feature&genres='+genre+'&start='+str(numpage)+'&explore=genres&ref_=adv_nxt')
        doc = fromstring(page.read())
        for div in doc.xpath("//div[@class='lister-item mode-advanced']"):
            imdb = div.xpath(".//div[@class='inline-block ratings-imdb-rating']")
            metacritc = div.xpath(".//div[@class='inline-block ratings-metascore']/span")
            title = div.xpath(".//h3/a")[0].text_content()
            year = div.xpath(".//h3/span[@class='lister-item-year text-muted unbold']")
            year = year[0].text_content().split()
            if len(year) > 0:
                try:
                    year = int(year[len(year) - 1].replace('(', '').replace(')', ''))
                except:
                    year = 0
                if title not in titles and len(imdb) > 0 and len(metacritc) > 0 and year >= min_year:
                    metascore = int(metacritc[0].text_content().replace('\n', '').replace(' ', ''))
                    imdbscore = int(float(imdb[0].text_content().replace('\n', '').replace(' ', '')) * 10)
                    # print title, metascore, imdbscore
                    if metascore + imdbscore >= min_media:
                        goodmovies.append({'title': title, 'imdb': imdbscore, 'metascore': metascore, 'year': year})

            titles.add(title)
        print 'pages:', analised
        analised += 1

print '-------------------------------------------------------'
print 'movies:', len(goodmovies)

goodmovies.sort(key=extractmedia, reverse=True)


with open('found_movies.csv', mode='w') as csv_file:
    fieldnames = ['title', 'imdb', 'metascore', 'year']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for movie in goodmovies:
        writer.writerow(movie)

# f = codecs.open("best movies3.txt", "w", "utf-8")
# f.write('titulo\t\tano\t\tmetascore\t\timdb\n')
#
# f.close()
