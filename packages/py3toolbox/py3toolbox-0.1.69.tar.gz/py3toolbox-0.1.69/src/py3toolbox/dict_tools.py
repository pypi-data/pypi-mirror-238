import json

try:
  from . import text_tools
except ImportError:
  import text_tools
  



def getdicv(dic, key):
  for k,v in dic.items():
    if k == key:
      return v
  return None

def walk_dic(dic):
  if isinstance(dic, dict): 
    for k, v in dic.items():
      if isinstance(v, dict) or isinstance(v, list):
        walk_dic(v)
      else:
        print("{0} : {1}".format(k, v))
  elif isinstance(dic, list):
    for d in dic:
      walk_dic(d)


if __name__ == "__main__": 
  a = {"a.b" : "123"}
  print (getdicv(a,"a.b"))

  with open("R:/1.json", "r") as content:
    dic = json.loads(content.read())

  result = []
  result = walk_dic1(dic, result)
  print ("\n".join(result))

  pass