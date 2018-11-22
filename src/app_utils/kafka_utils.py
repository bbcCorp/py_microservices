from confluent_kafka import Producer, Consumer, KafkaError

class SimpleKafkaMessage():
    def __init__(self,
        topic:str = None,
        partition:int = None,
        offset:int = None,
        message:str = None
    ):
        self._topic = topic
        self._partition = partition
        self._offset = offset
        self._message=message


    @property
    def topic(self):
        return self._topic


    @property
    def partition(self):
        return self._partition

    @property
    def offset(self):
        return self._offset

    @property
    def message(self):
        return self._message            

  
###############################################################################
class SimpleKafkaProducer():

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

        if not config:
            config = {'bootstrap.servers': 'localhost:9092'}

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

########################## End of KafkaProducer ###############################

###############################################################################
class SimpleKafkaConsumer():

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

        if not config:
            config = {
                'bootstrap.servers': 'localhost:9092',
                'group.id': 'mygroup',
                'client.id': 'client-1',
                'enable.auto.commit': True,
                'session.timeout.ms': 6000,
                'default.topic.config': {'auto.offset.reset': 'smallest'}
            }

        self._consumer = Consumer(config)

        msg = 'Kafka consumer has been setup.'
        if self.logger:
            self.logger.debug(msg)
        else:
            print(msg)

    ###########################################################################
    def consume(self, topics : list, process_flag=True):
        '''
            This is a generator function that returns a stream of SimpleKafkaMessage.
            Pass a list of topics to consume
        '''
        self._consumer.subscribe(topics)
        try:
            while process_flag:
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