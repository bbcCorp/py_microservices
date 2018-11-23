import json
from abc import ABCMeta, abstractmethod
from confluent_kafka import Producer, Consumer, KafkaError

###############################################################################
class IKafkaMessage(object):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def topic(self):
        pass


    @property
    @abstractmethod
    def partition(self):
        pass

    @property
    @abstractmethod
    def offset(self):
        pass

    @property
    @abstractmethod
    def message(self):
        pass

    @abstractmethod
    def serialize(self):
        pass

    @classmethod
    def deserialize(serialized_message):
        pass

###############################################################################
class SimpleKafkaMessage(IKafkaMessage):
    '''
        This is a simple message format which accepts string as message
        It uses JSON format to serialize itself.
    '''
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

    def serialize(self):
        return json.dumps(self.__dict__)

    @classmethod
    def deserialize(serialized_message):
        entity = json.loads(serialized_message)

        _topic = None,
        _partition = None,
        _offset = None,
        _message = None

        if 'topic' in entity:
            _topic = entity['topic']

        if 'partition' in entity:
            _partition = entity['partition']

        if 'offset' in entity:
            _offset = entity['offset']

        if 'message' in entity:
            _message = entity['message']

        return SimpleKafkaMessage(
            topic=_topic, 
            partition=_partition, 
            offset=_offset, 
            message=_message)

 ###############################################################################