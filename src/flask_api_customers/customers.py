import os
import sys
import unittest
import logging
from datetime import datetime
import json

from flask import Flask, request
from flask_restful import Resource

import settings as CONST

curpath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join (curpath, "../")))

from app_models import Customer
from app_utils import MongoRepository, DbEntity

class CustomerAPI(Resource):

    def __init__(self):
        #Create and configure logger 
        logfile= os.path.abspath("{0}/{1}".format(CONST.log_settings["log_folder"], CONST.log_settings["log_file"]))        
        os.makedirs( os.path.dirname(logfile), exist_ok=True)

        logging.basicConfig(
            filename=logfile, 
            format='%(asctime)s %(message)s', 
            filemode='a'
        ) 

        #Creating an object 
        self.logger=logging.getLogger() 
        
        #Setting the threshold of logger to DEBUG 
        self.logger.setLevel(CONST.log_settings["log_level"])                     

        self.entity = "customers"
        self.repo = MongoRepository(logger=self.logger, 
            server=CONST.db_customer["url"],
            port=CONST.db_customer["port"], 
            database=CONST.db_customer["db"], 
            collection=self.entity, 
            session_id=1)        

    ###########################################################################
    # GET /customers
    # GET /customers/1
    def get(self,id=None):
        '''
            Used to read one records
        '''

        if id:
            msg = 'Processing request to get {0} with id:{1}'.format(self.entity, id)
            self.logger.debug(msg)            
        else:
            msg = 'Processing request to get all {0}'.format(self.entity)
            self.logger.debug(msg)

        try:
            if id:
                records = self.repo.find_by_id(id)
            else:
                records = [c for c in self.repo.fetchall()]       
            
            return json.dumps(records), 200

        except Exception as e:
            msg = 'Error in processing GET request.', str(e)
            self.logger.error(msg)

            return { 'status' : 'error' }, 500
    ###########################################################################
    # POST /customers
    def post(self):
        ''' 
            Used to create entity
        '''
        self.logger.debug('Processing POST request')

        if not request.data:
            msg = "Request to create entity needs to come with form 'data' "
            self.logger.error(msg)
            return { 
                'status' : 'error',
                'msg' : msg                 
            }, 400

        try:                        
            entity = Customer( json=json.loads(request.data) )

            wellformed, msg = entity.isValid()
            if not wellformed:
                self.logger.error(msg)
                return { 
                    'status' : 'error',
                    'msg' : msg                 
                }, 400            

            result = self.repo.create(entity)

            return { 'status' : 'success' }, 200

        except Exception as e:
            msg = 'Error in processing POST request.', str(e)
            self.logger.error(msg)

            return { 'status' : 'error' }, 500

    ###########################################################################
    # PUT /customers/id
    def put(self, id=None):
        ''' 
            Used for update
        '''
        if (not id) or (not request.data):
            msg = "Request to update entity needs to come for a specific entity id and 'data' "
            self.logger.error(msg)
            return { 
                'status' : 'error',
                'msg' : msg                 
            }, 400


        msg = 'Processing request to update entity:{0} with id:{1}'.format(self.entity, id)

        try:
            entity = Customer( json=json.loads(request.data) ) 

            wellformed, msg = entity.isValid()
            if not wellformed:
                self.logger.error(msg)
                return { 
                    'status' : 'error',
                    'msg' : msg                 
                }, 400

            result = self.repo.update_by_id(id,entity)            
            return { 'status' : 'success' }, 200 

        except Exception as e:
            msg = 'Error in processing PUT request.', str(e)
            self.logger.error(msg)

            return { 'status' : 'error' }, 500

    ###########################################################################
    # DELETE /customers/id
    def delete(self, id):
        ''' 
            Used for update
        '''

        msg = 'Processing request to delete entity:{0} with id:{1}'.format(self.entity, id)
        self.logger.debug(msg)
       
        try:
            result = self.repo.delete_by_id(id)

            return { 'status' : 'success' }, 200

        except Exception as e:
            msg = 'Error in processing DELETE request.', str(e)
            self.logger.error(msg)

            return { 'status' : 'error' }, 500


    ###########################################################################
    
###############################################################################