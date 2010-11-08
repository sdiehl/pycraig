# Quick and dirty in memory database, which supports pickeling

from pickle import dumps, loads, dump, load

class Table:

    def __init__(self):
        self.index = 0
        self.schema = None
        self.rows = []

    def insert(self,row):
        # Take the schema of the first row and insist that all
        # subsequent rows have the same
        if not self.schema:
            self.schema = row.schema

        if row.schema != self.schema:
            raise Exception('Schema mismatch')

        self.rows.append(row)
        self.index = len(self.rows)

    def __iter__(self):
        return iter(self.rows)

    def __len__(self):
        return len(self.rows)

    def dump(self):
        return dumps(self)

    def to_file(self,fn):
        fp = open(fn, 'wb')
        dump(self,fp)
        fp.close()

    @staticmethod
    def from_file(fn):
        fp = open(fn, 'rb')
        up = load(fp)
        fp.close()
        return up

    @staticmethod
    def load(dump):
        return loads(dump)

class Row(object):
    cols = {}
    schema = None

    def __init__(self,**columns):
        self.cols = {}
        self.schema = hash(tuple(columns.keys()))
        for col, val in columns.iteritems():
            self.cols[col] = val

    def __getattr__(self,key):
        if key in self.cols:
            return self.cols[key]
        return object.__getattribute__(self, key)

    def __len__(self):
        return len(self.cols)
