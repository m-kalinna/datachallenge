#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import tarfile
import subprocess
import shutil
import re
from pyspark.sql import SparkSession

class SparkConnector:

    def __init__(self, cores):
        #enable logging
        self.logger = logging.getLogger('SparkConnector')
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        #create connection to local spark cluster
        master_uri = "local[" + str(cores) + "]"
        self.spark = SparkSession \
            .builder \
            .master(master_uri) \
            .appName("Python Spark SQL basic example") \
            .getOrCreate()


    def run_query(self, query, limit = 200):
        """runs the query and prints results in a pretty format"""
        self.spark.sql(str(query)).show(limit)


    def return_query(self, query):
        """runs the query and returns result as list of row objects"""
        return self.spark.sql(str(query)).collect()
    

    def load_table(self, filename):
        """
        Loads specified .json into a table. For now, we only dump
        the data into views.
        """
        tablename = re.search('[^_\/]+.json', filename).group().rsplit('.')[0]
        self.logger.info('Loading ' + filename + ' into table ' + tablename)
        df = self.spark.read.json(str(filename))
        df.createOrReplaceTempView(tablename)
        self.logger.info(filename + ' was loaded into table ' + tablename)


    def extract_tar(self, filename):
        """
        creates a local directory in /tmp and extracts all
        files from given tar to it. returns tmp folder name.
        """
        local_tmp = None
        local_tmp = subprocess.check_output('mktemp -d', shell=True).rstrip()
        self.logger.info('Extracting ' + filename + ' to ' + local_tmp)
        tar = tarfile.open(filename)
        tar.extractall(path=local_tmp)
        tar.close()
        self.logger.info('Extraction finished')
        return local_tmp


    def load_tables_from_tar(self, filename):
        """
        we consume all jsons from this tar and put them
        into tables
        """
        local_tmp = self.extract_tar(filename)
        # now we loop over all .json files in dir and load them
        for root, dirs, files in os.walk(local_tmp):
            for f in files:
                if f.endswith('.json'):
                    self.load_table(os.path.join(root,f))
        # we have to remove local_tmp
        # shutil.rmtree(local_tmp)
