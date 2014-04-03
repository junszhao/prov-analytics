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


simpleAssociationQuery = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
    select distinct ?activity ?agent
    where {?activity prov:wasAssociatedWith ?agent}
    """

qualifiedAssociationquery = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
    select distinct ?activity ?agent
    where {?activity prov:qualifiedAssociation [prov:agent ?agent]}
    """




simpleUsageQuery = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
    select distinct ?activity ?entity
    where {?activity prov:used ?entity}
    """

qualifiedUsagequery = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
    select distinct ?activity ?entity
    where {?activity prov:qualifiedUsage [prov:entity ?entity]}
    """




simpleDerivationQuery = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
    select distinct ?entity1 ?entity2
    where {?entity1 prov:wasDerivedFrom ?entity2}
    """

qualifiedDerivationQuery = """
    PREFIX prov: <http://www.w3.org/ns/prov#>
    select distinct ?entity1 ?entity2
    where {?entity1 prov:qualifiedDerivation [prov:entity ?entity2]}
    """


simpleGenerationQuery = """
        PREFIX prov: <http://www.w3.org/ns/prov#>
        select distinct ?entity ?activity
        where {?entity prov:wasGeneratedBy ?activity}
        """
    
qualifiedGenerationQuery = """
        PREFIX prov: <http://www.w3.org/ns/prov#>
        select distinct ?entity ?activity
        where {?entity prov:qualifiedGeneration [prov:activity ?activity]}
"""


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


    def query(self,g, query):
        data = self.sparql("/sparql/endpoint-lax/"+g, query)
        
        return data


    def rewriteQualifiedAssociation(self,g):
        outfilename = g+'newAssociations.nt'
        outfile = codecs.open(outfilename, mode='w', encoding='UTF-8')
        
        newTriples = self.query(g, qualifiedAssociationquery)
        
        triples = 0
        
        
        for binding in newTriples["results"]["bindings"]:
            
            activity = binding["activity"]["value"]
            agent = binding["agent"]["value"]
            triple = "<" + activity + "> \t <http://www.w3.org/ns/prov#wasAssociatedWith> \t" + "<" + agent + "> .\n"
            triples = triples +1
            outfile.write(triple)
            outfile.flush()
        
        outfile.close()
        
        print str(triples) + " new associations are added"
        
        return


    def rewriteQualifiedUsage(self,g):
        outfilename = g+'newUsage.nt'
        outfile = codecs.open(outfilename, mode='w', encoding='UTF-8')
        
        newTriples = self.query(g, qualifiedUsagequery)

        triples = 0
        
        for binding in newTriples["results"]["bindings"]:
            
            activity = binding["activity"]["value"]
            entity = binding["entity"]["value"]
        
            triple = "<" + activity + "> \t <http://www.w3.org/ns/prov#used> \t" + "<" + entity + "> .\n"
            triples = triples +1
            outfile.write(triple)
            outfile.flush()
    
        print str(triples) + " new usage are added"
        
        outfile.close()
        
        return


    def rewriteQualifiedGeneration(self,g):
        outfilename = g+'newGeneration.nt'
        outfile = codecs.open(outfilename, mode='w', encoding='UTF-8')
        
        newTriples = self.query(g, qualifiedGenerationQuery)
        
        triples = 0
        
        
        for binding in newTriples["results"]["bindings"]:
            
            entity = binding["entity"]["value"]
            activity = binding["activity"]["value"]
        
            triple = "<" + entity + "> \t <http://www.w3.org/ns/prov#wasGeneratedBy> \t" + "<" + activity + "> .\n"
            triples = triples +1
            outfile.write(triple)
            outfile.flush()
        
        outfile.close()
        
        print str(triples) + " new generations are added"
        
        return


    def rewriteProv(self,filename):
        
        print "==== Rewrite " + filename + "===="
        
        self.rewriteQualifiedGeneration(filename)
    #    
    #    self.rewriteQualifiedDerivation(filename)
    #    
        self.rewriteQualifiedUsage(filename)
    #
        
        self.rewriteQualifiedAssociation(filename)
        
        
        
        return


    def main(self):
        
        #endpointpath = ["ta-provenance", "csiro", "obiama"]
        
        for arg in self.endpointpath:
            self.rewriteProv(arg)
        return

    def __init__(self):
        self.endpointpath = ["ta-provenance", "csiro", "obiama"]
        self.endpointhost = "http://www.open-biomed.org.uk/sparql/endpoint-lax/"

if __name__ == "__main__":
    ProvRewrite().main()

#if __name__ == "__main__":
#    main()
#
#




