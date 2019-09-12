>>> # Problem 2
...
>>> x_1 = int(2.3)     #create an integer.
>>> type(x_1)          #type of object is integer.
<class 'int'>
>>> x_2 = x_1          #create a copy.
>>> x_2 = "Saharnaz"   #change the new (copied) object.
>>> x_2 == x_1         #compare the two objects
False                  #Only new one changed
>>> type(x_1)
<class 'int'>
>>> type(x_2)
<class 'str'>
>>> #int is immutable
>>>
>>>
>>> y_1 = str(1989)   #create a string
>>> type(y_1)
<class 'str'>
>>> y_2 = y_1          #create a copy of the object
>>> y_2 = 1989      #change new object
>>> y_1 == y_2         #test for change
False
>>> type(y_2)
<class 'int'>
>>> print(y_1, y_2)
1989 1989         #Only one changed (looks same but one object is integer, the other one is string)
# str is immutable
>>>
>>> list1 = list([1, 2, 3]) #create a list
>>> list2 = list1      #new copy of list
>>> list2[1] = 'a'     #change new list
>>> print([[list1], [list2]]) #Both changed!
[[1, 'a', 3], [1, 'a', 3]]
>>> # list is mutable
>>>
>>> tuple1 = ('Jonathan', 'Milton', 'Leili') #create new tuple
>>> tuple2 = tuple1     #new name for tuple
>>> tuple2 += ('Saharnaz',) #change new tuple
>>> tuple1 == tuple2    #compare tuples
False                   #Only one tuple changed
>>> print(tuple1, tuple2)
(('Jonathan', 'Milton', 'Leili') ('Jonathan', 'Milton', 'Leili', 'Saharnaz'))
>>> # tuple is immutable
>>>
>>> set1 = {'alpha', 'alpha', 'a', 10} #create new set
>>> set2 = set1         #new name for the set
>>> set2 -={'alpha'}    #change the new set
>>> print(set1, set2)   #Both changed
{10, 'a'} {10, 'a'}
>>> #set is muttable
