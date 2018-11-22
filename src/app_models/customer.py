import os
import sys

curpath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join (curpath, "../")))

from app_utils import DbEntity

###############################################################################
class Customer(DbEntity):
    def __init__(self, id=None, name=None, phone=None, email=None, json=None):
        
        super().__init__() 
        self.id = -1
        self.name = None
        self.phone = None
        self.email = None

        if json:
            if 'id' in json:        
                self.id = json['id']
            
            if 'name' in json:
                self.name = json['name']
            
            if 'phone' in json:
                self.phone = json['phone']
            
            if 'email' in json:
                self.email = json['email']

        if id:
            self.id = id

        if name:
            self.name = name
        
        if phone:
            self.phone = phone

        if email:
            self.email = email

    def isValid(self):

        if (self.id == -1):
            return False , "Invalid entity. 'id' needs to be set"

        if (not self.name):
            return False , "Invalid entity. 'name' needs to be set"

        if (not self.phone):
            return False , "Invalid entity. 'phone' needs to be set"

        if (not self.email):
            return False , "Invalid entity. 'email' needs to be set"

        return True , "Valid entity"

###############################################################################
if __name__ == "__main__":
    test = Customer(id=1, name="BBC", phone="1-800-PHONE", email="test@email.com")
    print("Object JSON:{0}".format(test.toJSON()))      

###############################################################################    