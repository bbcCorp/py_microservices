import uuid
import json
import copy
from datetime import datetime, date

from enum import IntEnum, unique

@unique
class AppEventType(IntEnum):
    '''
        Various application events are represented by this enum
        We are using IntEnum to make it serializable
    '''
    Any = 0,
    Insert = 100,
    Update = 200,
    Delete = 300    

    def __str__(self):
        return '{0}:{1}'.format(self.name, self.value)

###############################################################################
class AppEventArgs():

    def __init__(self, 
        app_event_type:AppEventType = AppEventType.Any, 
        before_change:str = None, 
        after_change:str  =None):
        
        self.id = str(uuid.uuid4())
        self.event_ts = datetime.now().isoformat()
        self.app_event_type = app_event_type
        self.before_change = None
        self.after_change = None

        if before_change:
            self.before_change = copy.deepcopy(before_change)
        
        if after_change:
            self.after_change = copy.deepcopy(after_change)

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
            default=AppEventArgs.json_default,
            sort_keys=True
        ).encode('utf-8')

############################################################################### 
###############################################################################
