# Problem 2
x_1 = int(2.3)
print(type(x_1))
x_2 = x_1
x_2 = "Saharnaz"
print(x_2 == x_1)
print(type(x_1))
print(type(x_2))
# int is immutable

y_1 = str(1989)
print(type(y_1))
y_2 = y_1
y_2 = 1989
print(type(y_2))
print(y_1, y_2)
# str is immutable

list1 = list([1, 2, 3])
list2 = list1
list2[1] = 'a'
print([[list1], [list2]])
# list is mutable

tuple1 = ('Jonathan', 'Milton', 'Leili')
tuple2 = tuple1
tuple2 += ('Saharnaz',)
print(tuple1 == tuple2)
print(tuple1, tuple2)
# tuple is immutable

set1 = {'alpha', 'alpha', 'a', 10}
set2 = set1
set2 -={'alpha'}
print(set1, set2)
#set is muttable
