#!/usr/bin/env python2.4

import sys, os, re
#from pysqlite2 import dbapi2 as sqlite

import MySQLdb as mysql

#con = sqlite.connect("shirts.db")
con = mysql.connect(host='mysql.dsandler.org', user='dsandler',
    passwd=open('.dbpasswd').read().strip(), db='dsandlerdb')

cur = con.cursor()

for fn in os.listdir("thumb"):
    if not re.search(r'\.jpg$', fn): continue
    cur.execute("select count(*) from shirts where filename = %s", (fn,))
    count = cur.fetchone()[0]
    print fn, count
    if count == 0:
        try:
            (year, college, rest) = re.match(r'^([^-]+)[.-]([^-]+)-(.+).jpg$', fn).groups()
            if college not in ('sid', 'wrc', 'gsa', 'baker', 'brown',
            'wiess', 'jones', 'martel', 'mcmurtry', 'hanszen',
            'lovett', 'duncan'):
                print "error: unknown college in file %s" % fn
                sys.exit(1)
        except Exception, e:
            print "exception on file %s: %s" % (fn, `e`)
            sys.exit(1)

        rest = rest.split('-')
        if len(rest) == 1:
            face = rest[0]; variant = None
        else:
            variant, face = rest[0:2]
        cur.execute("""insert into shirts 
                (added, college, year, face, variant, filename) 
            values (NOW(), %s, %s, %s, %s, %s)""",
                (college, year, face, variant, fn)
            )
        print "imported %s" % fn
con.commit()
        
