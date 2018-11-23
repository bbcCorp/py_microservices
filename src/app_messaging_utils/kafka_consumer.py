from abc import ABCMeta, abstractmethod
from .kafka_message import IKafkaMessage, SimpleKafkaMessage
from confluent_kafka import Consumer, KafkaError


###############################################################################
class IKafkaConsumer(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def configure(self, config):
        pass

    @abstractmethod
    def consume(self, topics : list):
        pass

###############################################################################
class SimpleKafkaConsumer(IKafkaConsumer):
    '''
        A simple consumer class for Kafka Queue
        
    '''
    def __init__(self, logger=None, config=None):
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
        self._consumer = Consumer(config)

        msg = 'Kafka consumer has been setup using config:', config
        if self.logger:
            self.logger.debug(msg)
        else:
            print(msg)        

    ###########################################################################
    def consume(self, topics : list):
        '''
            This is a generator function that returns a stream of SimpleKafkaMessage.
            Pass a list of topics to consume
        '''

        assert isinstance(topics, list), "`topics` should be of type `list`."

        self._consumer.subscribe(topics)
        try:
            while True:
                msg = self._consumer.poll(0.1)
                if msg is None:
                    continue

                elif not msg.error():
                    # self.logger.debug('Received message: {0}'.format(msg.value()))

                    yield SimpleKafkaMessage(
                        topic=msg.topic(), 
                        partition=msg.partition(),
                        offset=msg.offset(),
                        message = msg.value()  
                    )

                elif msg.error().code() == KafkaError._PARTITION_EOF:  
                    _err = 'End of partition reached {0}/{1}'.format(msg.topic(), msg.partition())

                    if self.logger:                  
                        self.logger.error(_err)
                    else:
                        print(_err)
                
                else:
                    _err = 'Error occured: {0}'.format(msg.error().str())

                    if self.logger:                  
                        self.logger.error(_err)
                    else:
                        print(_err)

        except Exception as e:
            _err = 'Error occured: {0}'.format( str(e) ) 

            if self.logger:                  
                self.logger.error(_err)
            else:
                print(_err)

        finally:
            self._consumer.close()

########################## End of KafkaConsumer ###############################