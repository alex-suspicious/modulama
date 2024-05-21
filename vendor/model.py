from vendor.data import data

class model(object):
    table = ""
    attributes = {}
    variables = {}

    def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        instance.__init__(*a, **kw)
        return instance

    def include(self, shared, request):
        pass

    def __init__(self, table = None):
        if( table != None ):
            self.table = table
        elif( self.table == "" ):
            self.table = type( self ).__name__ + "s"

        self.data = data(self.table, self.attributes)
        pass

    def where(self, A = "", B = "=", C = "", create = False):
        self.data.where(A, B, C, create)
        return self

    def first(self):
        self.data.load()
        self.data.first()

        tempKeys = list(self.data.variables.keys())
        for x in range(len(self.data.variables)):
            setattr( self, tempKeys[x], self.data.variables[tempKeys[x]] )

        return self

    def save(self):
        variables = vars(self)
        keys = list(variables.keys())
        self.data.variables = {}

        for x in range(len(variables)):
            if( keys[x] in self.attributes ):
                self.data.variables[ keys[x] ] = variables[keys[x]]

        self.data.save()