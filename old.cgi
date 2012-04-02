#!/usr/bin/python2.2

import sys, cgi, cgitb, re

cgitb.enable()

# copied from http://www.earthgatetours.com/jencooper/shirts/
files = [
  '1980-wrc-front.jpg',
  '1981-wrc-back.jpg',
  '1981-wrc-front.jpg',
  '1984-wrc-front.jpg',
  '1986-lovett-front.jpg',
  '1987-wrc-front.jpg',
  '1988-wrc-front.jpg',
  '1989-wrc-front.jpg',
  '1990-wrc-front.jpg',
  '1991-wrc-front.jpg',
  '1993-wrc-front.jpg',
  '1994-wrc-front.jpg',
  '1995-wrc-front.jpg',
  '1997-wrc-front.jpg',
  '1998-wrc-front.jpg',
  '1999-wrc-sweep-back.jpg',
  '1999-wrc-sweep-front.jpg',
  '2000-wrc-front.jpg',
  '2001-wrc-front.jpg',
  '2002-wrc-front.jpg',
]

class Shirt:
    def __init__(self, filename):
        self.filename = filename
        parts = filename.split('-')
        self.year = int(parts[0])
        self.college = parts[1]
        self.side = parts[-1]
        if len(parts) > 3:
            self.extra = parts[2]
        else:
            self.extra = None
    def __repr__(self):
        return "[Shirt: %s %s %s (%s)]" % (self.year, self.college,
        self.side, self.extra)

class ShirtDB:
    def __init__(self, files):
        self.shirts = [Shirt(x) for x in files]
        self.reindex()

    def reindex(self):
        self.years = {}
        for s in self.shirts:
            if not self.years.has_key(s.year):
                self.years[s.year] = [s]
            else: self.years[s.year].append(s)

        self.colleges = {}
        for s in self.shirts:
            if not self.colleges.has_key(s.college):
                self.colleges[s.college] = [s]
            else: self.colleges[s.college].append(s)

    def listAll(self): return self.shirts
    def listCollege(self, co):
        if self.colleges.has_key(co): return self.colleges[co]
        return []
    def listYear(self, yr):
        yr = int(yr)
        if self.years.has_key(yr): return self.years[yr]
        return []

def main():
    db = ShirtDB(files)

    form = cgi.FieldStorage()
    sys.stdout.write("Content-type: text/html\n\n")

    results = db.listAll()
    
    if form.has_key("year"):
        results = filter(lambda x: x.year == int(form['year'].value),
            results)
    if form.has_key("college"):
        results = filter(lambda x: x.college == form['college'].value,
            results)
    
    print results

if __name__ == '__main__':
    main()
