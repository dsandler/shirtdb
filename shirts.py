class Shirt:
    def __init__(self, filename):
        self.filename = filename
        parts = filename.split('.')[0].split('-')
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
        self.filtered = self.shirts[:]

    def results(self): return self.filtered
    def filterOn(self, key, value):
        self.filtered = filter(
            lambda x: getattr(x,key)==value,
            self.filtered)

    def allYears(self):
        y = {}
        for s in self.shirts: y[s.year] = 1
        l = y.keys() ; l.sort() ; return l
    def allColleges(self):
        y = {}
        for s in self.shirts: y[s.college] = 1
        l = y.keys() ; l.sort() ; return l
