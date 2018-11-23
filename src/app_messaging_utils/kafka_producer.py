from abc import ABCMeta, abstractmethod
from confluent_kafka import Producer


###############################################################################
class IKafkaProducer(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def configure(self, config):
        pass

    @abstractmethod
    def produce(self, topic, message, key=None, callback=None):
        pass

########################## End of IKafkaProducer ##############################

###############################################################################
class SimpleKafkaProducer(IKafkaProducer):

    def __init__(self, logger=None):
        '''
            Param:
            * logger: an instance of python logger class 
            * config: a dictionary of configuration parameters.
                    The only required property is bootstrap.servers 
                    which is used to specify the address of one or more 
                    brokers in a Kafka cluster. 
        '''
        self.logger = logger

    ###########################################################################
    def configure(self, config):
        '''
            Param:
            * config: a dictionary of configuration parameters.
                    The only required property is bootstrap.servers 
                    which is used to specify the address of one or more 
                    brokers in a Kafka cluster. 
        '''        
        self._producer = Producer(config)

        if self.logger:
            self.logger.debug('Kafka producer has been setup.')

    ###########################################################################
    def produce(self, topic, message, key=None, callback=None):
        '''
            Both the key and value parameters need to be either 
            * a byte-like object (in Python 2.x this includes strings)
            * a Unicode object 
            * None. 
        '''

        # debug = "topic:{0} :: message:{1}".format(topic, message)
        # print(debug)

        self._producer.produce(topic, key=key, value=message, callback=callback)

        # The flush method blocks until all outstanding produce commands have completed
        # self._producer.flush(30)

########################## End of SimpleKafkaProducer##########################
