"""prov-analysis.py: Some basic prov-o benchmarking
    
    Usage: prov-analysis.py
    """

import os, os.path
import sys
import re
import unittest
import logging
import httplib
import urllib
import time
import StringIO
import codecs
import csv


try:
    # Running Python 2.5 with simplejson?
    import simplejson as json
except ImportError:
    import json


from ProvRewrite import ProvRewrite

class TestProvRewrite(unittest.TestCase):

    def setUp(self):
        super(TestProvRewrite, self).setUp()
        return

    def tearDown(self):
        super(TestProvRewrite, self).tearDown()
        return
    
    def assertBindingEqual(self, data, count, msg):
        bindings = len(data)
        self.assertEqual(bindings, count, msg)


    def testDetectDuplicateAssociations(self):
        
        associations = {'file:///mnt/open-biomed-data/oxford/workspace/wf4ever/provenance-corpus/Taverna_repository/workflow_1052_version_1/run_1/workflowrun.prov.ttl#taverna-prov-export','file:///mnt/open-biomed-data/oxford/workspace/wf4ever/provenance-corpus/Taverna_repository/workflow_1052_version_1/run_1/workflowrun.prov.ttl#taverna-engine'}
        
        data = ProvRewrite().simpleAssociation("ta-provenance")
        return self.assertBindingEqual(data, 192, "Wrong.")
    


if __name__ == "__main__":
    unittest.main()
