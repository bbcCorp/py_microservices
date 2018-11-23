###############################################################################
#  Process to read Customer Updates                                           #
#
#  Pre-requisites: Kafka server should be running                             #
###############################################################################
import os
import sys
import logging
import json 

import settings as SETTINGS

curpath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join (curpath, "../")))

from app_messaging_utils import SimpleKafkaConsumer, SimpleKafkaMessage
from app_models import Customer, AppEventType
from app_utils import MongoRepository, DbEntity

###############################################################################

class MessageProcessor():

    def __init__(self, process_func=None):
        
        #Create and configure logger 
        logfile = os.path.abspath('{0}/{1}'.format(SETTINGS.Logging["LogFolder"],SETTINGS.Logging["LogFile"]))        
        os.makedirs(os.path.dirname(logfile), exist_ok=True)

        logging.basicConfig(
            filename=logfile, 
            format='%(asctime)s %(message)s', 
            filemode='a'
        ) 

        #Creating an object 
        self.logger=logging.getLogger() 
        
        #Setting the threshold of logger to DEBUG 
        self.logger.setLevel(SETTINGS.Logging["LogLevel"]) 

        self.config = SETTINGS.KafkaService
        self.topic  = SETTINGS.MESSAGE_TOPIC

        self.customer_repo = MongoRepository(
            logger=self.logger, 
            server=SETTINGS.MongoDB["Url"],
            port=SETTINGS.MongoDB["Port"], 
            database=SETTINGS.MongoDB["Db"], 
            collection=SETTINGS.MongoDB["Collection"], 
            session_id=1)

    ###########################################################################
    def process_message(self, evt_msg: SimpleKafkaMessage):
        '''
            Function to process SimpleKafkaMessage

            Deserialize the SimpleKafkaMessage, 
            extract and process relevant payload
        '''
        try:

            evt = json.loads(evt_msg.message)

            if evt["app_event_type"] == AppEventType.Insert:
                entity = evt["after_change"]
                customer = Customer(
                    id=entity["id"], 
                    name=entity["name"], 
                    phone=entity["phone"],
                    email=entity["email"]
                )
                
                msg="Processing INSERT message for customer id:{0}".format(customer.id)
                print(msg)

                eid = self.customer_repo.create(customer)  # expect to get back an ObjectId  

                msg="Created customer id:{0}".format(customer.id)
                print(msg)
                self.logger.debug(msg)


            elif evt["app_event_type"] == AppEventType.Update:
                entity = evt["after_change"]
                customer = Customer(
                    id=entity["id"], 
                    name=entity["name"], 
                    phone=entity["phone"],
                    email=entity["email"]
                )
                
                msg="Processing UPDATE message for customer id:{0}".format(customer.id)
                print(msg)

                self.customer_repo.update_by_id(customer.id, customer)  
                msg="Updated customer id:{0}".format(customer.id)
                print(msg)
                self.logger.debug(msg)


            elif evt["app_event_type"] == AppEventType.Delete:
                entity = evt["after_change"]
                customer = Customer(
                    id=entity["id"], 
                    name=entity["name"], 
                    phone=entity["phone"],
                    email=entity["email"]
                )
                
                msg="Processing DELETE message for customer id:{0}".format(customer.id)
                print(msg)

                self.customer_repo.delete_by_id(customer.id)  

                msg="Deleted customer id:{0}".format(customer.id)
                print(msg)
                self.logger.debug(msg) 

            else:
                pass               

        except Exception as e:
            msg = "Error in process_message function: {0}".format(str(e))
            print(msg)
            self.logger.error(msg)
      
    ###########################################################################
    def read_messages(self):
        '''
            Function to read messages from kafka queue 
        '''
        reader_id = self.config["group.id"]
        counter=0
    
        try:
            msg = "Starting Process:{0} to read topic:{1} from Kafka Queue".format( reader_id , self.topic )
            self.logger.info(msg)
            print(msg)

            consumer = SimpleKafkaConsumer(logger=self.logger)
            consumer.configure(config=self.config)
            
            print ("Starting Consumer")
            for evt_msg in consumer.consume(topics=['MICROSERVICE-CUSTOMER-UPDATES']):
                
                counter +=1

                # msg = "Received msg: {0} # {1}".format(counter, evt_msg.message)
                # print(msg)
                # self.logger.debug(msg)

                # Process the message
                self.process_message(evt_msg)
        
        except KeyboardInterrupt:
            msg = "\n\n Exiting Process:'{0}'. {1} message(s) read on topic from Kafka Queue:'{2}'".format( reader_id, counter, self.topic )
            print (msg)
            self.logger.info(msg)

        except Exception as e:
            msg = "Error in {0} : {1}".format(reader_id, str(e))
            print(msg)
            self.logger.error(msg)

###############################################################################
if __name__ == "__main__":

    MessageProcessor().read_messages()

###############################################################################    