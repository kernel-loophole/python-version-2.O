# -*- coding: utf-8 -*-
#multiple constructor
class person:
  def __init__(self,*args):
    if len(args)>1:
      sum=0
      for i in range(0,len(args)):
        sum=sum+args[i]
      self.value=sum
      
    elif isinstance(args[0],str):
      self.value="hello this str"+args[0]
    elif isinstance(args[0],int):
      self.value=args[0]*args[0]
    elif isinstance(args[0],list):
      self.value=max(args[0])

c1=person(1,2,3)
c2=person(12)
c3=person("str")
c4=person([1,4,5,6,7])
print(c1.value)
print(c2.value)
print(c3.value)
print(c4.value)

