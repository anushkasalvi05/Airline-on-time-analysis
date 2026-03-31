#%%
print("My name is anushka.", "My age is 25")
#print("my age is 25")
print(25+58)

#%%
name="anushka"
age = 25
price = 25.99
print(name + age + price)

#%%
name = "anushka"
age = 25
price = 25.99

print(name)
print(age)
print(price)

print(f"my name is {name} and my age is {age}.")

print(type(name))
print(type(age))
print(type(price))

#%%
#print sum
a = 50
b = 120

sum = a + b
print("The total sum is : ", sum)

diff = a - b
print("The difference is : ", diff)

#%%
#comments

#This is a comment
print("Hello World")          # Beginner code

""" 
This 
is a 
multiline 
comment
"""

#%%
#arithmetic operators
a = 5
b = 2

sum = a+b

print(f" The sum is : {sum}")
print(a-b)
print(a*b)
print(a%b)            #remainder
print(a ** b)

#%%
#comparison

x = 30
y = 50

print(x == y)
print(x != y)
print(x > y)
print(x < y)

#%%
#write a program to input 2 numbers and print their sum
num1 = int(input("Enter your first number: "))
num2 = int(input("Enter your second number: "))

sum = num1 + num2

print(f"The sum of he numbers you entered is: {sum}")

#%%
#Write a program to input side of a square and print its area

side_of_square = float(input("Enter side length: "))

area = (side_of_square * side_of_square)

print(f"The area of the sqaure is: {area}")

#%%
#Write a program to input two floating point numbers and print their average

f1 = float(input("Enter your first floating point number: "))
f2 = float(input("Enter your second floating point number: "))

average = (f1 + f2)/2
print(f"The average is: {average}")

#%%
#Write a program to input two int numbers (a & b). Print True if a is greater than equal to b. If not, print False
a1 = int(input("Enter first: "))
b1 = int(input("Enter second: "))

print(a >= b)

#%%
str1 = "This is a string"
str2 = 'This is also a string'
str3 = """this is another way to write a string"""

#finalstr = str1 + str2 + str3
#print(finalstr)

print(len(str1))

#%%
#indexing
str4 = "Anushka Salvi"

ch = str4[7]
print(ch)

#%%
#slicing
str5 = "Apna College"

print(str5[5:])

#%%
str = "i am studying python"

print(str.endswith("ng"))
print(str.capitalize())
print(str.replace("python", "R"))
print(str.find("s"))
print(str.count("am"))

#%%
#Write  a program to input user's first name and print its length

name = input("Enter your name here: ")

print(f"Your name is {name} and the total characters in your name are: {len(name)}")

#%%
#Write a program to find the occurence of '$' in a string
str29 = "this is just a $ and more $ and $"

print(str29.count("$"))

#%%
#conditional statements
age = int(input("Enter your age: "))

if age >= 18:
    print("You can apply for a driver's license")
elif age >= 16 and age < 18:
    print("You can apply for a learner's permit")
else:
    print("You are underage. Please refrain from driving")

#%%
marks = int(input("Please enter your marks here:"))

if marks >= 90:
    print("Grade A")
elif marks >= 80 and marks < 90:
    print("Grade B")
elif marks >= 70 and marks < 80:
    print("Grade C")
else:
    print("Grade D")

#%%
age = int(input("Please enter age:"))

if age >= 18:
    if age >= 75:
        print("Cannot drive")
    else:
        print("Can Drive")
else:
    print("Cannot Drive")

#%%
num29 = int(input("Enter number: "))

if num29 % 2 == 0:
    print("Even number")
else:
    print("odd number")

#%%
a = int(input(("number 1")))
b = int(input(("number 2")))
c = int(input(("number 3")))

if a >= b and a >= c:
    print("A is the largest number")
elif b >= a and b >= c:
    print("B is the largest number")
else:
    print("C is the largest number")

#%%
i = int(input("Enter a number: "))
if i % 7 == 0:
    print("Multiple of 7")
else:
    print("Not multiple of 7")
