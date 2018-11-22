###############################################################################
# Unit Tests for the flask version of customer API
#
#  Pre-requisites: Flask API server should be running   
###############################################################################
import os
import sys
import unittest
import json
from datetime import datetime
from requests import put, get, post, delete, head, codes

import test_settings as CONST

curpath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join (curpath, "../")))

from app_models import Customer

###############################################################################
class CustomerApiTests(unittest.TestCase):

   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api_baseurl = CONST.api_url
        self.testdate = datetime.now().strftime('%Y-%m-%d')
        self.testid = CONST.test_id

   def test001_CustomerAPI_CRUD(self):

        headers = {
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }

        # Test GetAll
        api = self.api_baseurl
        print("\n GET:: ", api)
        try:
            response = get(api, headers=headers)            
            data = json.loads(response.json())
            print("GET::",data)

            self.assertEqual(response.status_code, codes.ok)
        except Exception as e:
            msg = "Error with GET:{0} \n {1}".format(api, str(e))
            print(msg)

        # Test Create
        api = self.api_baseurl      
        print("\n POST:: ", api)  
        try:
            record = Customer(id=1, name="BBC", phone="1-800-Phone", email="bbc@email.com").toJSON()
            response = post(api, headers=headers, data=record)
            print("POST::",response)

            self.assertEqual(response.status_code, codes.ok)
        except Exception as e:   
            msg = "Error with POST:{0} \n {1}".format(api, str(e))
            print(msg)
            return

        # Test Update
        api = "{0}/{1}".format(self.api_baseurl, 1)
        print("\n PUT:: ", api)
        try:
            record = Customer(id=1, name="BBC", phone="1-800-Phone-Updated", email="bbc@email.com").toJSON()
            response = put(api, headers=headers, data=record)
            print("PUT::",response)

            self.assertEqual(response.status_code, codes.ok)
        except Exception as e:   
            msg = "Error with PUT:{0} \n {1}".format(api, str(e))
            print(msg)

        # Test GetByID
        api = "{0}/{1}".format(self.api_baseurl, 1)
        print("\n GET:: ", api)
        try:
            response = get(api, headers=headers)
            print("GET by id::",response)
            print(response.json())

            self.assertEqual(response.status_code, codes.ok)
        except Exception as e:
            msg = "Error with GET:{0} \n {1}".format(api, str(e))
            print(msg)


        # Test Delete
        api = "{0}/{1}".format(self.api_baseurl, 1)
        print("\n DELETE:: ", api)
        try:
            response = delete(api, headers=headers)
            print("DELETE::",response)

            self.assertEqual(response.status_code, codes.ok)
        except Exception as e:   
            msg = "Error with DELETE:{0} \n {1}".format(api, str(e))
            print(msg)       


        # Test Count
        api = self.api_baseurl
        print("\n GET:: ", api)
        try:
            response = get(api, headers=headers)
            print("GET::",response)
            data = json.loads(response.json())

            self.assertEqual(response.status_code, codes.ok)
            self.assertEqual(len(data), 0)

        except Exception as e:
            msg = "Error with GET:{0} \n {1}".format(api, str(e))
            print(msg)

###############################################################################
if __name__ == '__main__':
    unittest.main()
###############################################################################