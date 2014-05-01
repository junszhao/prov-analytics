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

def sparql(path, query):
    params = urllib.urlencode({"query": query})
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "application/sparql-results+json"}
    conn = httplib.HTTPConnection("www.open-biomed.org.uk")
    conn.request('POST', path, params, headers)
    res = conn.getresponse()
    if (res.status != 200):
        print res.status
        print res.reason
        print res.read()
        conn.close()
        return None
    else:
        resultSet = json.load(res)
        conn.close()
        return resultSet










def getProperties (g):
    sparqlquery = """
        select distinct ?p
        where {?s ?p ?o .
        }
        """
    data = sparql("/sparql/endpoint-lax/"+g, sparqlquery)
    
    properties = []
    
    for binding in data["results"]["bindings"]:
        
        properties.append(binding)
    
    print len(properties)
    return








def analyse(filename):
    
    
    print "==== Analyse " + filename + "===="
                    
    getProperties(filename)
                    
    return


def main():
                    
    #endpointpath = ["ta-provenance", "csiro", "obiama"]
    
    endpointpath = ["ta-provenance"]
                    
    endpointhost = "http://www.open-biomed.org.uk/sparql/endpoint-lax/"
    
    for arg in endpointpath:
        analyse(arg)

if __name__ == "__main__":
    main()
