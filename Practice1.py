class Dog:
    def __init__(self, name, breed, owner):
        self.name = name
        self.breed = breed
        self.owner = owner
    def bark(self):
        print("woof woof")

class Owner:
    def __init__(self, name, address, contact_number): #This is like a constructor in java 
        self.name = name
        self.address = address 
        self.phone_number = contact_number
        
owner1 = Owner("COllins","Tacoma","467")
owner2= Owner("Pesh","coma","4897")
dog1 = Dog("Bruce", "Greyhound",owner1)
#print(dog1.owner.name)
"""dog1.bark()
print(dog1.breed)
print(dog1.name)"""

dog2 = Dog("F", "GH", owner2) # when you create an object of a class you are instantiating the class to create an instance of the class
#print(dog2.owner.address)


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hello, my name is  {self.name} and I an {self.age} years old.")

"""person1 = Person("Alice", 30)
person1.greet()

person3 = Person("BOBER", 30)
person3.greet()"""

from datetime import datetime
class User:
    def __init__(self, username, email, password):
        self.username = username
        self._email = email  #protected data by prefixing _ not to be used outside class but can be if very necessary
        self.__password = password # private data by __ cannot be used 
        #private and protected can be accessed inside the class, protected can be accessed outside class but private
        # variables cannot be accessed outside of class, protected generally are more used. 

    def say_hi_to_user(self, user):
        print(f"Sending message to {user.username}: hi {user.username} its {self.username}")
    def clean_email(self):
        return self._email.lower().strip()
    def get_email(self):
        print(f"email accessed at {datetime.now()}")
        return self._email
    
    def set_email(self, new_email):
        if "@" in new_email:
            self._email = new_email

user1 = User("DAN", " DAN@gmail.com ", "PASS")
user2 = User("COLLO", " COLLO@gmail.com ","SAPP")

user1.say_hi_to_user(user2)

print(user1.get_email())
user1.set_email("GMAfsfsfsfsfsdfsf@sdfssdfsdfasdfasdfadf")
print(user1.get_email())
#print(user1.email)
#print(user1._email)
#print(user1.clean_email())
#user1.email = 123421
#print(user1.email)