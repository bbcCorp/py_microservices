import os
import sys
from datetime import date, datetime
import logging
import random
import copy
import json

from pymongo import MongoClient, ReturnDocument
import bson
from bson import json_util
from bson.objectid import ObjectId

from .db_entity import DbEntity

###############################################################################
class MongoRepository():
    def __init__(self, logger, server,port, database, collection, session_id=None):
        '''
            server: mongo server url
            port: mongo server port
            collection: mongo collection for a particular object
        '''

        # Configure the logger
        if session_id is None:
            session_id=random.randint(0,1024)
        self.logger = logging.LoggerAdapter(logger, { 'session_id': session_id })

        self.logger.debug("Connecting to {0}:{1}".format(server, port))
        self.client = MongoClient(server, port)

        self.logger.debug("Accessing collection {0} in database:{1}".format(collection, database))
        self.db = self.client[database]
        _collections = self.db.collection_names(include_system_collections=False)
        if collection not in _collections:
            print("Warning: Collection {0} does not exist. A new collection will be created.".format(collection))
        
        self.collection = self.db[collection]
            
    ###########################################################################
    def create(self, entity: DbEntity):
        '''
            api to create entity. Returns newly created entity id if successful
        '''
        try:
            result =  self.collection.insert_one( entity.__dict__ )

            self.logger.info('Created entity id:{0} of type:{1}'.format(result.inserted_id, self.collection))
            return result.inserted_id

        except Exception as e:
            self.logger.error('Error creating entity {0}::{1}'.format(self.collection, str(e)))
            raise

    ###########################################################################
    def update(self, criteria, entity:DbEntity):
        '''
            api to update entity. Performs a replacement.
        '''
        try:
            if id != entity["id"]:
                msg = "Entity id:{0} in the request and the object:{1} does not match".format(id, entity["id"])
                raise ValueError(msg)

            entity.updated_on = datetime.isoformat(datetime.now())

            update_criteria = copy.deepcopy(criteria) 
            update_criteria["deleted"] = False
            result = self.collection.replace_one(update_criteria, entity.__dict__)

            if result.matched_count == 0:
                msg = "Could not find entity id:{0} of type:{1}".format(id, self.collection)
                raise ValueError(msg)

            self.logger.info('Updated {0} entities of type:{1} matching criteria:{2}'.format(result.modified_count, self.collection, criteria))
            return result.modified_count == 1

        except Exception as e:
            self.logger.error('Error updating entity {0} with id:{1}::{2}'.format(self.collection, id, str(e)))
            raise    

    ###########################################################################
    def update_by_id(self, id, entity:DbEntity):
        '''
            api to update entity. Performs a replacement.
        '''
        try:
            if id != entity.id:
                msg = "Entity id:{0} in the request and the object:{1} does not match".format(id, entity["id"])
                raise ValueError(msg)

            criteria = { "id": id, "deleted": False }

            old_entity = self.collection.find_one(criteria)
            if not old_entity:
                msg = "Entity id:{0} does not exist in the database".format(id)
                raise ValueError(msg)

            
            entity.updated_on = datetime.isoformat(datetime.now())
            
            updated_entity = entity.__dict__
            updated_entity['_id'] = old_entity['_id']
            
            result = self.collection.replace_one(criteria, updated_entity)

            if result.matched_count == 0:
                msg = "Could not find entity id:{0} of type:{1}".format(id, self.collection)
                raise ValueError(msg)

            self.logger.info('Updated {0} entities of type:{1} matching criteria:{2}'.format(result.modified_count, self.collection, criteria))
            return result.modified_count == 1

        except Exception as e:
            self.logger.error('Error updating entity {0} with id:{1}::{2}'.format(self.collection, id, str(e)))
            raise    

    ###########################################################################
    def update_fields(self, id, updated_fields:dict):
        '''
            api to update entity. Updates part of the object
        '''
        try:
            if not id:
                msg = "Entity id:{0} needs to be passed for update operation".format(id)
                raise ValueError(msg)

            criteria = { "id": id , "deleted": False }

            update_request = copy.deepcopy(updated_fields)
            update_request["updated_on"] = datetime.isoformat(datetime.now())

            result = self.collection.update_one(criteria, { "$set": update_request })

            if result.matched_count == 0:
                msg = "Could not find entity id:{0} of type:{1}".format(id, self.collection)
                raise ValueError(msg)

            self.logger.info('Updated {0} entities of type:{1} matching criteria:{2}'.format(result.modified_count, self.collection, criteria))
            return result.modified_count == 1

        except Exception as e:
            self.logger.error('Error updating entity {0} with id:{1}::{2}'.format(self.collection, id, str(e)))
            raise           

    ###########################################################################
    def delete_by_id(self, id):
        '''
            soft deletes document matching document id
        '''           
        try:

            criteria = {"id": id, "deleted": False }
            update = { "$set": { "deleted": True, "updated_on": datetime.isoformat(datetime.now()) } }
            result =  self.collection.update_one(criteria, update)

            self.logger.info('Deleted {0} entities of type:{1} matching criteria:{2}'.format(result.modified_count, self.collection, criteria))
            return result.modified_count == 1
        
        except Exception as e:
            self.logger.error('Error deleting entity {0} with id:{1}::{2}'.format(self.collection, entity_id, str(e)))
            raise    

    ###########################################################################    
    def delete(self, criteria:dict):
        '''
            soft deletes all documents matching search criteria
        '''
        try:
            self.logger.debug('Attempting deletion of entities {0} matching criteria:{1}'.format(self.collection, criteria))
            
            update = { "$set": { "deleted": True, "updated_on": datetime.isoformat(datetime.now()) } }
            result =  self.collection.update_many(criteria, update)

            self.logger.info('Deleted {0} entities of type:{1} matching criteria:{2}'.format(result.modified_count, self.collection, criteria))
            return result.modified_count
        
        except Exception as e:
            self.logger.error('Error deleting entity {0} matching criteria:{1}::{2}'.format(self.collection, criteria, str(e)))
            raise            

    ###########################################################################
    def hard_delete_by_id(self, entity_id:ObjectId):
        '''
            hard deletes document matching document id.
            Does not consider delete flag
        '''        
        try:

            criteria = {"_id": ObjectId(entity_id)}

            self.logger.info('Attempting hard deletion of entity of type:{0} with id:{1}'.format(self.collection, entity_id))
            result =  self.collection.delete_one(criteria)

            self.logger.info('Hard deleted {0} entities of type:{1} matching criteria:{2}'.format(result.deleted_count, self.collection, criteria))
            return result.deleted_count == 1
        
        except Exception as e:
            self.logger.error('Error deleting entity {0} with id:{1}::{2}'.format(self.collection, entity_id, str(e)))
            raise    

    ###########################################################################
    def hard_delete(self, criteria:dict):
        '''
            hard deletes all documents matching search criteria.
            Does not consider delete flag
        '''
        try:
            self.logger.info('Attempting hard deletion of entities of type:{0} matching criteria:{1}'.format(self.collection, criteria))
            result =  self.collection.delete_many(criteria)

            self.logger.info('Hard deleted {0} entities of type:{1} matching criteria:{2}'.format(result.deleted_count, self.collection, criteria))
            return result.deleted_count
        
        except Exception as e:
            self.logger.error('Error deleting entity {0} matching criteria:{1}::{2}'.format(self.collection, criteria, str(e)))
            raise        

    ###########################################################################
    def fetchall(self):
        '''
            returns a generator function to iterate through all non-deleted
            documents in a collection
        '''        
        for c in self.collection.find({"deleted": False }):
            del c['_id']
            yield c

        return 

    ###########################################################################    
    def find(self, criteria:dict):
        '''
            returns a generator function to iterate through all non-deleted
            documents in a collection matching the given criteria
        '''         
        search_criteria = copy.deepcopy(criteria)
        search_criteria["deleted"] = False

        for c in self.collection.find(search_criteria):
            del c['_id']
            yield c

        return      

    ###########################################################################
    def find_by_id(self, id):
        criteria = {"id": id, "deleted": False }
        result = self.collection.find_one(criteria)

        if result:
            del result['_id']    

        return result

    ###########################################################################
    def count(self, criteria):
        
        search_criteria = copy.deepcopy(criteria)
        search_criteria["deleted"] = False

        result = self.collection.count_documents(criteria)

        self.logger.debug('Database contains {0} entities of type:{1} matching criteria:{2}'.format(result, self.collection, criteria))
        return result

#################### End of MongoRepository ###################################    