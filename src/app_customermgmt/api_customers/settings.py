
import os

message_topic = 'MICROSERVICE-CUSTOMER-UPDATES'
message_producer = {
    "bootstrap.servers" : os.getenv('MICROSERVICES_KafkaService__Server') or "localhost:9092"
}