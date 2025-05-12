# Abstraction 
# Reduce complexity by hiding unnecessary details

class EmailService:
    def _connect(self):
        print("Connecting to email server")
    def _authenticate(self):
        print("Authenticating")
    def send_email(self):
        self._connect()
        self._authenticate()
        print("Sending email")
        self._disconnect()

    def _disconnect(self):
        print("Disconnecting from email server...")

email = EmailService()
#email.send_email() # just by providing this it allows user to focus on what an object does rather than how. user doesn't 
# need to know all the processes of sending email. 



### inheritance
# creating new classes based on existing classes parent-child class
# - A Car is-a Vehicle
# - A Bike is-a Vehicle 

### Polymorphism - ability of an object to take up many forms

class Vehicle:
    def __init__(self, brand, model, year):
        self.brand = brand 
        self.model = model
        self.year = year
    
    def start(self):
        print("V Is starting")

    def stop(self):
        print("Vehicle is stopping")
    
class Car(Vehicle):
    def __init__(self, brand, model, year, no_of_doors, 
                 no_of_wheels):
        super().__init__(brand,model,year)
        self.no_of_doors = no_of_doors
        self.no_of_wheels = no_of_wheels
class Bike(Vehicle):
    def __init__(self, brand, model, year, no_of_wheels):
        super().__init__(brand,model, year)
        self.no_of_wheels = no_of_wheels

class Truck(Vehicle):
    def __init__(self, brand,model, year, no_of_wheels):
        super().__init__(brand, model, year)
        self.no_of_wheels = no_of_wheels


car = Car("TOYOTA", "Focus", 7788, 5, 4)
bike = Bike("BIKE", "YODER", 232, 3)
truck = Truck("TRUCK", "Focus", 7788, 5)

print(car.__dict__)
print(bike.__dict__)
print(truck.__dict__)
car.start()
bike.start()


