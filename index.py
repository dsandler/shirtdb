#!/usr/bin/python

import web, os, sys, random

DEBUG = True

COLLEGES = dict(
    wrc='Will Rice',
    sid='Richardson',
    hanszen='Hanszen',
    lovett='Lovett',
    baker='Baker',
    wiess='Wiess',
    brown='Brown',
    jones='Jones',
    martel='Martel',
    gsa='GSA',
)

urls = (
    r'/',                      'site',
    r'/search',                'search_stub',
    #r'/show/?',                'show_all',
    r'/show/([0-9]+)/?',       'show_year',
    r'/show/([^/]+)/?',           'show_college',
    r'/show/([^/]+)/([0-9]+)/?',  'show_college_year',
    r'/show/([^/]+)/([0-9]+)/(.*)/?',  'show_college_year',
)

render = web.template.render('templates/', cache=False)

G = web.Storage(
    path='',
    sorted=sorted,
    colleges=COLLEGES,
    subhead=lambda:"%s&ndash;%s" % (earliest_year(),latest_year()),
    decade_of=lambda y:int(y)/10*10,
)

_cache = web.Storage()

def get_all_years():
    global _cache
    if not 'all_years' in _cache:
        _cache.all_years = [(x.year, x.count) for x in web.select('shirts', what='count(*) as count, year', order='year', group='year')]
    return _cache.all_years
G.get_all_years = get_all_years

def earliest_year():
    return get_all_years()[0][0]

def latest_year():
    return get_all_years()[-1][0]

def random_shirts(num):
    all_ids = [str(x.uid) for x in web.select('shirts', what='uid')]
    random.shuffle(all_ids)
    assortment = all_ids[0:num]
    return web.select('shirts', where='uid in (%s)' % ','.join(assortment))

def recent_shirts(num):
    return web.select('shirts', order='added desc', limit=num)

######################################################################

class search_stub:
    def GET(self):
        i = web.input()
        if 'year' in i and i.year != '':
            web.redirect('/show/%d' % int(i.year))
        elif 'college' in i and i.college != '' and i.college in COLLEGES:
            web.redirect('/show/%s' % i.college)
        else:
            web.redirect('/')

class site:
    def GET(self):
        print render.index(G, recent_shirts, random_shirts)

class show_all:
    def GET(self):
        print render.index(G, "Not implemented.")

class show_year:
    def GET(self, year):
        print render.year(
            G,
            year,
            web.select('shirts', 
                where='shirts.year = %s' % web.db.sqlify(year),
                order='college, variant'))

class show_college:
    def GET(self, college):
        print render.college(
            G,
            college,
            COLLEGES[college] + " College", 
            web.select('shirts', 
                where='shirts.college = %s' % #' and shirts.face = \'front\'' %
                    web.db.sqlify(college),
                group='variant, year',
                order='year, variant')
        )

class show_college_year:
    def GET(self, college, year, variant=None):
        where = 'shirts.college = %s and shirts.year = %s' % \
            (web.db.sqlify(college), web.db.sqlify(year))
        if variant is not None:
            where += ' and shirts.variant = %s' % web.db.sqlify(variant)
        shirts = web.select('shirts', 
            where = where,
            order ='variant')

        variants = {}
        for s in shirts:
            if s.variant not in variants:
                variants[s.variant] = {}
            variants[s.variant][s.face] = s
                
        print render.college_year(
            G,
            college,
            COLLEGES[college] + " College", 
            year,
            variants)



if __name__ == "__main__": 
    if DEBUG:
        web.webapi.internalerror = web.debugerror

    web.config.db_parameters = dict(dbn='mysql', db='dsandlerdb',
        host='mysql.dsandler.org', user='dsandler', pw='Tur60ing')

    #def runfcgi_apache(func):
    #    web.wsgi.runfcgi(func, None)

    #web.wsgi.runwsgi = runfcgi_apache
    #web.runwsgi = web.runfcgi

    #web.run(urls, globals(), web.reloader)
    web.run(urls, globals())

