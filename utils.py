
def getAttributes(cls):   
  return [i for i in cls.__dict__.keys() if i[:1] != '_']