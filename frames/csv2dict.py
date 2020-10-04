import os

class csv2dict():
  data = {} # Dictionary to store the entries
  
  def __init__(self,keyFilePath=None):
    try:
      if keyFilePath is None:
        keyFilePath = ".keys.txt"

      lines = [line.rstrip('\n') for line in open(keyFilePath)]

      for line in lines:
        line_s = line.split(',')
        self.data[line_s[0]] = line_s[1]

    except FileNotFoundError:
      print('MISSING .keys.txt unable to load keys')

  ###
  # Retrieve a value from the data storage
  ###
  def get(self,key):
    if str(key) in self.data:
      return self.data[str(key)]
    return None