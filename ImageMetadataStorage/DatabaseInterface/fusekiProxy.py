import tornado.ioloop
import tornado.web
import logging
import requests
from rdflib import Graph, Literal, RDF, URIRef, Namespace
import urllib
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('Provider')
import json
import uuid

#Enables adding new image to the database.
class addImageData(tornado.web.RequestHandler):

    async def post(self):
        request_path = self.request.path
        try:
            URL = "http://localhost:3030/constructionSiteRiskData/update"
            payload = self.request.body.decode('utf-8')
            _logger.info("payload submitted to fuseki: " + payload)

            jsonUpdate = json.loads(payload)
            insertStatement = 'PREFIX so: <http://www.semanticweb.org/safetyOntology#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> INSERT DATA { so:' + str(uuid.uuid1()) + ' rdf:type so:Image ; so:hasImageId "' + jsonUpdate["imageID"] + '" ; so:hasRiskRelatedObject "' + jsonUpdate["name"] + '" ; so:hasConfidence "' + jsonUpdate["confidence"] + '" ; so:hasXmax "' + jsonUpdate["xmax"] + '" ; so:hasXmin "' + jsonUpdate["xmin"] + '" ; so:hasYmax "' + jsonUpdate["ymax"] + '"; so:hasYmin "' + jsonUpdate["ymin"] + '"; so:hasImageURL "' + jsonUpdate["imageURL"] + '"; so:hasAnchorBoxImageURL "' + jsonUpdate["anchorBoxImageURL"] + '" .}'

            response = requests.post(URL + '?update=', data = insertStatement)
            _logger.info("response received from fuseki: " + str(response.text))
        except Exception as e:
            _logger.info("Error happened: "+ str(e))

#Enables quering image metada. Accepts SPARQL query statement as input parameter
class queryImageData(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    async def post(self):
        request_path = self.request.path
        try:
            URL = "http://localhost:3030/constructionSiteRiskData/query"
            payload = self.request.body.decode('utf-8')
            payload = urllib.parse.quote(payload)
            _logger.info("payload submitted to fuseki: " + URL + '?query=' + payload)
            x = requests.get(URL + '?query=' + payload)
            results = json.loads(x.text)
            responseResults = str(results["results"])
            print(responseResults.replace("'", '"'))
            self.write(responseResults.replace("'", '"'))

        except Exception as e:
            _logger.info("Error happened: "+ str(e))

#Allows deleting all content stored in the database
class deleteImageData(tornado.web.RequestHandler):

    async def post(self):
        request_path = self.request.path
        try:
            URL = "http://localhost:3030/constructionSiteRiskData/update"
            payload = self.request.body.decode('utf-8')
            _logger.info("payload submitted to fuseki333: " + payload)

            insertStatement = 'DELETE {?d ?c ?u} WHERE{?d ?c ?u}'

            response = requests.post(URL + '?update=', data = insertStatement)
            _logger.info("response received from fuseki: " + str(response.text))
        except Exception as e:
            _logger.info("Error happened: "+ str(e))



    def options(self):
        self.set_status(204)
        self.finish()

#Defines the endpoints for accessing provided functionalities
application = tornado.web.Application([
    (r'/fusekiAddImage', addImageData),
    (r'/fusekiQueryData', queryImageData),
    (r'/clearFuseki', deleteImageData)
])


if __name__ == "__main__":
    _logger.info("Starting tornado server")
    application.listen(8084)
    tornado.ioloop.IOLoop.instance().start()
