#####################################################
#       Unit Tests for the Kafka Messaging          #
#
#  Pre-requisites: Kafka server should be running   #
#####################################################
import os
import sys
import unittest
import logging
from datetime import datetime
import test_settings as CONST

curpath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join (curpath, "../")))

from app_utils import SimpleKafkaConsumer, SimpleKafkaMessage, SimpleKafkaProducer

###############################################################################
class SimpleMessagingTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.testdate = datetime.now().strftime('%Y-%m-%d')
        self.testid = CONST.test_id

        #Create and configure logger 

        logfile= os.path.abspath("{0}/kafka_messaging_tests_{1}-{2}.log".format (CONST.log_settings["log_folder"], self.testdate,self.testid))
        os.makedirs(os.path.dirname(logfile), exist_ok=True)

        logging.basicConfig(
            filename=logfile, 
            format='%(asctime)s %(message)s', 
            filemode='a'
        ) 

        #Creating an object 
        self.logger=logging.getLogger() 
        
        #Setting the threshold of logger to DEBUG 
        self.logger.setLevel(CONST.log_settings["log_level"])                     

    
    ############################################################################
    def test001_ProduceAndConsumeMessages(self):

        test_topic = "KafkaMessagingTest_{0}_{1}".format(self.testdate, self.testid)

        producer = SimpleKafkaProducer(logger=self.logger, config=CONST.KAFKA_CONFIG["producer"])
        
        print ("Starting Producer")
        for i in range(0,100):
            msg = "Test Message {0}:{1}:{2}".format(self.testdate, self.testid, i)
            producer.produce(topic=test_topic,message=msg)
            print("Sent msg {0}: {1}".format(i,msg))
        print ("Completed sending 100 messages")
        
        
        consumer = SimpleKafkaConsumer(logger=self.logger, config=CONST.KAFKA_CONFIG["consumer"])
        counter=1
        continueFlag=True

        print ("Starting Consumer")
        for msg in consumer.consume(topics=[test_topic], process_flag=continueFlag):

            print("Received msg: {0} # {1}".format(counter, msg.message))
            counter +=1

            if counter == 100:
                continueFlag = False
                break

        print ("Completed receiving 100 messages")    

    
    ############################################################################
    def test002_ConsumeApplicationMessages(self):

        consumer = SimpleKafkaConsumer(logger=self.logger, config=CONST.KAFKA_CONFIG["consumer"])
        counter=1
        continueFlag=True

        print ("Starting Consumer")
        for msg in consumer.consume(topics=[ 'MICROSERVICE-CUSTOMER-EMAIL-NOTIFICATION', 'MICROSERVICE-CUSTOMER-UPDATES'  ], process_flag=continueFlag):

            print("Received msg: {0} # {1}".format(counter, msg.message))
            counter +=1

            if counter == 10:
                continueFlag = False
                break

        print ("Completed receiving 10 application messages")         

###############################################################################
if __name__ == '__main__':
    unittest.main()
###############################################################################