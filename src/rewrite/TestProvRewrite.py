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
        
        associations = {'file:///mnt/open-biomed-data/oxford/workspace/wf4ever/provenance-corpus/Taverna_repository/workflow_1052_version_1/run_1/workflowrun.prov.ttl#taverna-prov-export':'file:///mnt/open-biomed-data/oxford/workspace/wf4ever/provenance-corpus/Taverna_repository/workflow_1052_version_1/run_1/workflowrun.prov.ttl#taverna-engine'}
        
        qualifed = ProvRewrite().qualifiedAssociation("ta-provenance")
        data = ProvRewrite().compare(qualifed, associations)
        
        return self.assertEqual(len(data), 0, "This triple should not be added.")
    
    def testDetectNewAssociations(self):
    
        associations = {'http://ns.taverna.org.uk/2011/run/9a816c93-fe28-41b7-b352-6a3de3a98588/process/3aae8073-f726-480d-8ad1-8e2f446952b1/':'file:///mnt/open-biomed-data/oxford/workspace/wf4ever/provenance-corpus/Taverna_repository/workflow_1833_version_1/run_1/workflowrun.prov.ttl#taverna-engine'}
        
        simple = ProvRewrite().simpleAssociation("ta-provenance")
        data = ProvRewrite().compare(simple, associations)
        
        print data
    
        return self.assertEqual(len(data), 1, "This triple should be added.")


if __name__ == "__main__":
    unittest.main()
