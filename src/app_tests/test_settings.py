import logging
from datetime import datetime

test_id='001'

db_customer={
    "url" : "mongodb://root:pwd123@localhost",
    "port": 27017,
    "db"  : "py_microservices_unittests-{0}-{1}".format(datetime.now().strftime("%Y-%m-%d"),test_id)
}

log_settings = {
    "log_folder" : "./logs",
    "log_level"  : logging.DEBUG

}

flask_api_url = "http://localhost:5000/customers"
django_api_url = "http://localhost:8000/api/customers/"