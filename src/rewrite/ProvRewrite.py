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


class ProvRewrite(object):

    def sparql(self,path, query):
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


    def simpleAssociation(self,g):
        query = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            select distinct ?activity ?agent
            where {?activity prov:wasAssociatedWith ?agent}
            """
        data = self.sparql("/sparql/endpoint-lax/"+g, query)
        
        associations = {}

        for binding in data["results"]["bindings"]:

            activity = binding["activity"]["value"]
            agent = binding["agent"]["value"]
            associations[activity]=agent
        
        print len(associations)
        return associations




    def qualifiedAssociation(self,g):
        query = """
            PREFIX prov: <http://www.w3.org/ns/prov#>
            select distinct ?activity ?agent
            where {?activity prov:qualifiedAssociation [prov:agent ?agent]}
            """
        data = self.sparql("/sparql/endpoint-lax/"+g, query)
        
        associations = {}
        
        for binding in data["results"]["bindings"]:
            
            activity = binding["activity"]["value"]
            agent = binding["agent"]["value"]
            associations[activity]=agent
        
        print len(associations)
        return associations
            
            
            

    def compare(self, simple, newTriples):
        
        newEntityKeys = newTriples.keys()
        
        newAssociations = {}

        for key in newEntityKeys:
            
            newTriple = newTriples[key]
            
            if simple.has_key(key):
            
                if (simple[key]!=newTriple):
                    newAssociations[key]= newTriple

            else:
                newAssociations[key]= newTriple
        return newAssociations



    def rewriteQualifiedAssociation(self,g):
        
        self.compare(self.simpleAssociation(g), self.qualifiedAssociation(g))
        
#        associations = self.simpleAssociation(g)
#        
#        newAssociations ={}
#        
#        query = """
#            PREFIX prov: <http://www.w3.org/ns/prov#>
#            select distinct ?activity ?agent
#            where {?activity prov:qualifiedAssociation [prov:agent ?agent]}
#            """
#        data = self.sparql("/sparql/endpoint-lax/"+g, query)
#        
#        for binding in data["results"]["bindings"]:
#
#            activity = binding["activity"]["value"]
#            agent = binding["agent"]["value"]
#            
#            if associations.has_key(activity):
#            
#                if (associations[activity]!=agent):
#                    newAssociations[activity]= agent
#                    print "<"+activity + ">\t<http://www.w3.org/ns/prov#wasAssociatedWith>\t<" + agent + ">"
#            else:
#                newAssociations[activity]= agent
#                print "<"+activity + ">\t<http://www.w3.org/ns/prov#wasAssociatedWith>\t<" + agent + ">"
#
#        print str(len(newAssociations)) + " new association relationships added"

        return


    def rewriteProv(self,filename):
        
        print "==== Rewrite " + filename + "===="
        
    #    rewriteQualifiedGeneration(filename)
    #    
    #    rewriteQualifiedDerivation(filename)
    #    
    #    rewriteQualifiedUsage(filename)
    #    
        self.rewriteQualifiedAssociation(filename)
        
        return


    def main(self):
        
        #endpointpath = ["ta-provenance", "csiro", "obiama"]
        
        for arg in self.endpointpath:
            self.rewriteProv(arg)
        return

    def __init__(self):
        self.endpointpath = ["ta-provenance"]
        self.endpointhost = "http://www.open-biomed.org.uk/sparql/endpoint-lax/"

if __name__ == "__main__":
    ProvRewrite().main()

#if __name__ == "__main__":
#    main()
#
#




