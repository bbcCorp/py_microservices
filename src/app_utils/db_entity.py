import json
from datetime import date, datetime

class DbEntity(object):

    def __init__(self):
        self.id = None

        self.created_on = datetime.isoformat(datetime.now())
        self.created_by = ""

        self.updated_on = datetime.isoformat(datetime.now())
        self.updated_by = ""

        self.deleted = False

    ##########################################################################
    @staticmethod
    def json_default(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat() 
        else:
            return obj.__dict__

    ##########################################################################
    def toJSON(self):
        return json.dumps(self, 
            ensure_ascii=False, 
            default=DbEntity.json_default,
            sort_keys=True
        ).encode('utf-8')

###############################################################################          