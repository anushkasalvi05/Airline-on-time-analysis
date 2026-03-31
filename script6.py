
#%%
marks = [94.4, 97.4, 87.8, 45.1, 66.4]

print(marks)
print(type(marks))

#%%
print(marks[0])
print(len(marks))

#%%
student = ["Karan", 95.4, 17, "Delhi"]

#print(student[1:4])
print(student[-3:-1])

#%%
list1 = [2,1,3,5]

list1.append(4)
print(list1)

list1.sort()       #ascending 1,2,3,4,5
print(list1)

list1.sort(reverse=True)    #descending 5,4,3,2,1
print(list1)

list2 = ["Banana", "Mango", "Apple"]
list2.sort()
print(list2)

list2.reverse()
print(list2)

list1.reverse()
print(list1)

list1.insert(1,6)
print(list1)

list2.remove("Mango")
print(list2)

list1.pop(2)
print(list1)

list2.


#%%
#tuples
tup1 = (1,2,3,4,5,1,2,3,3,3,3)
#print(type(tup1))
#print(tup1[0])
#print(tup1[1:4])
#tup=()

print(tup1.index(2))
print(tup1.count(3))


#%%
movies = []
mov1 = input("Enter first movie:")
mov2 = input("Enter second movie:")
mov3 = input("Enter third movie:")

movies.append(mov1)
movies.append(mov2)
movies.append(mov3)
print(movies)

#%%
empty_movies = []

empty_movies.append(input("Enter first movie name:"))
empty_movies.append(input("Enter second movie name:"))
empty_movies.append(input("Enter third movie name:"))

print(f"The list of three movies your entered are : {empty_movies}")


#%%
list1 = [1,2,1]
list2 = [3,4,5]

copy_list1 = list1.copy()
copy_list1.reverse()

if list1 == copy_list1:
    print("The list is a palindrome")
else:
    print("The list is not a palindrome")

copy_list2 = list2.copy()
copy_list2.reverse()

if list2 == copy_list2:
    print("The list is a palindrome")
else:
    print("The list is not a palindrome")



#%%
grade = ("c", "d","a","a","b","b","a")

print(grade.count("a"))


#%%
grade_list = ["c", "d","a","a","b","b","a"]

print(grade_list.sort())
print(grade_list)
