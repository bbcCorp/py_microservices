#####################################################
#       Unit Tests for the MongoRepository          #
#
#  Pre-requisites: Mongo server should be running   #
#####################################################
import os
import sys
import unittest
import logging
from datetime import datetime
import test_settings as CONST

curpath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join (curpath, "../")))

from app_models import Customer
from app_utils import MongoRepository, DbEntity

###############################################################################
class MongoRepositoryTests(unittest.TestCase):

   def __init__(self, *args, **kwargs):
        super(MongoRepositoryTests, self).__init__(*args, **kwargs)

        self.testdate = datetime.now().strftime('%Y-%m-%d')
        self.testid = CONST.test_id

        #Create and configure logger 

        logfile= os.path.abspath("{0}/mongo_repository_tests_{1}-{2}.log".format (CONST.log_settings["log_folder"], self.testdate,self.testid))
        os.makedirs(os.path.dirname(logfile), exist_ok=True)

        logging.basicConfig(
            filename=logfile, 
            format='%(asctime)s %(message)s', 
            filemode='a'
        ) 

        #Creating an object 
        logger=logging.getLogger() 
        
        #Setting the threshold of logger to DEBUG 
        logger.setLevel(CONST.log_settings["log_level"])                     

        self.repo = MongoRepository(logger=logger, 
            server=CONST.db_customer["url"],
            port=CONST.db_customer["port"], 
            database=CONST.db_customer["db"], 
            collection="customers", 
            session_id=1)

   ############################################################################
   def test001_CRUD(self):

        entity = Customer(id=0, name="Customer1", phone="1-800-Customer1")
        eid = self.repo.create(entity)  # expect to get back an ObjectId
        self.assertIsNotNone(eid , "Expect an id back for the newly created entity")

        records = [c for c in self.repo.fetchall()]
        self.assertEqual(len(records),1, "One entity should be returned")

        result = self.repo.find_by_id(entity.id)
        self.assertIsNotNone(result, "Object with the given id should be returned")

        self.assertTrue(self.repo.update_fields(entity.id, { "phone" : "1-800-Customer1-updated" }))

        self.assertTrue(self.repo.delete_by_id(entity.id), "We should be able to delete the object")

###############################################################################
if __name__ == '__main__':
    unittest.main()
###############################################################################
