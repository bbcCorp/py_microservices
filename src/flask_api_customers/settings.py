import logging
from datetime import datetime

app_settings = {
    "port" : 5000,

    "debug_mode": True
}

db_customer={
    "url" : "mongodb://root:pwd123@localhost",
    "port": 27017,
    "db"  : "py_microservices_api_customer"
}

log_settings = {
    "log_folder" : "./../../logs",
    "log_file" : "api-customer-{0}".format(datetime.now().strftime("%Y-%m-%d")),
    "log_level"  : logging.DEBUG
}