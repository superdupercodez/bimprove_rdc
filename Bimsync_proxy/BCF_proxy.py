import json
#import glob
#import os
import json
#import sys
import pprint
from urllib.request import urlopen

import tornado.ioloop
import tornado.web
import logging
import requests
#from rdflib import Graph, Literal, RDF, URIRef, Namespace
#import urllib

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('Provider')
#import uuid

def get_access_token(client_id, client_secret):
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = 'grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret

        response = requests.post('https://api.bimsync.com/oauth2/token', headers=headers, data=data)
        AT = response.json()["access_token"]
        return AT


def getBCFversion(ACCESS_TOKEN):
        print("Getting BCF version")
        headers = {
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'content-type': "application/json",
                }
        url = "https://bcf.bimsync.com/bcf/version"
        response = requests.request("GET", url, headers=headers)
        return response


def getBCFAllIssueBoards(ACCESS_TOKEN, PROJECT_ID):
        headers = {
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'content-type': "application/json",
        }
        #Asplunc
        url = "https://bcf.bimsync.com/bcf/beta/projects?bimsync_project_id=" + PROJECT_ID
        response = requests.request("GET", url, headers=headers)
        return response

def getBCFDocuments(ACCESS_TOKEN, BCF_PROJECT_ID):
        headers = {
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'content-type': "application/json",
        }
        #Asplunc
        url = "https://bcf.bimsync.com/bcf/beta/projects/" + BCF_PROJECT_ID + "/documents"
        response = requests.request("GET", url, headers=headers)
        return response

def createBCFTopic(ACCESS_TOKEN, BCF_PROJECT_ID, title, description):
        headers = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN,
        'content-type': "application/json",
        }

        url = "https://bcf.bimsync.com/bcf/beta/projects/" + BCF_PROJECT_ID + "/topics"

        mytitle = title
        mydescription = description

        payload = """
        {{"topic_type": "Info",
        "topic_status": "Open",
        "title": "{0}",
        "description": "{1}"
        }}"""
        print(payload.format(mytitle, mydescription))
        response = requests.request("POST", url, data=payload.format(mytitle, mydescription), headers=headers)
        pprint.pprint(response.json())
        return response

def createBCFComment(ACCESS_TOKEN, BCF_PROJECT_ID, TOPIC_ID, comment, viewPoint_guid):
        headers = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN,
        'content-type': "application/json",
        }
        url = "https://bcf.bimsync.com/bcf/beta/projects/" + BCF_PROJECT_ID + "/topics/" + TOPIC_ID + "/comments"


        mycomment = comment
        my_viewPoint_guid = viewPoint_guid

        payload = """{{
                "status": "Info",
        "verbal_status": "Open",
        "comment": "{0}",
        "viewpont_guid": "{1}"
        }}"""
        response = requests.request("POST", url, data=payload.format(mycomment, my_viewPoint_guid), headers=headers)
        pprint.pprint(response.json())
        return response


def createBCFViewpoint(ACCESS_TOKEN, BCF_PROJECT_ID, TOPIC_ID):
        headers = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN,
        'content-type': "application/json",
        }
        print("BCF_PROJECT_ID", BCF_PROJECT_ID)
        print("TOPIC_ID", TOPIC_ID)
        #url = "https://bcf.bimsync.com/bcf/beta/projects/" + BCF_PROJECT_ID + "/topics/" + TOPIC_ID + "/viewpoints"
        url = "https://opencde.bimsync.com/bcf/2.1/projects/" + BCF_PROJECT_ID + "/topics/" + TOPIC_ID + "/viewpoints"
        payload = """{

                    "bitmaps": [{
                        "location": {
                                "x": 21.97304764097038,
                                "y": -24.86912390497038,
                                "z": 19.66912390497035
                        },
                        "normal": {
                            "x": -0.5773502691896258,
                            "y": 0.5773502691896258,
                            "z": -0.5773502691896258
                        },
                        "up": {
                            "x": -0.4082482904638631,
                            "y": 0.4082482904638631,
                            "z": 0.8164965809277261
                        },
                        "bitmap_data": "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"
                    }],
                    "snapshot": {
                        "snapshot_data": "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"
                    }
                }
        }"""
        response = requests.request("POST", url, data=payload, headers=headers)
        pprint.pprint(response.json())
        return response

def uploadBCFSnapshot(ACCESS_TOKEN, BCF_PROJECT_ID, TOPIC_ID, viewpointGuid, filePath):
        url = "https://bcf.bimsync.com/bcf/beta/projects/" + BCF_PROJECT_ID + "/topics/" + TOPIC_ID + "/viewpoints/" + viewpointGuid +  "/snapshot"
        if (filePath.startswith('http')):
            fileData = urlopen(filePath).read()

        else:
            fileData = open("/var/cells/data/bimprove/processed/" + filePath, 'rb').read()

        #print(fileData)

        headers = {
        'Authorization': 'Bearer ' + ACCESS_TOKEN,
        'content-type': "application/binary",
        }
        response = requests.put(url,data=fileData,headers=headers)
        return response
        # NB: Ref snapshot above. There is also a bitmap feature that is richer, including positioning in 3D and indicating normal vector


class addImageData(tornado.web.RequestHandler):


    async def post(self):
        request_path = self.request.path
        try:
            payload = self.request.body.decode('utf-8')
            jsonUpdate = json.loads(payload)
            ACCESS_TOKEN = get_access_token("e3MLbLz5LCDlMls", "DMBxORv9iNQDDJC")
            issue_board_id = "3f41f1bf7bd3430792a6d008edc6895b"
            #create topic
            topicAnswer = createBCFTopic(ACCESS_TOKEN, issue_board_id, "ImageId_" + jsonUpdate["imageID"], "Detected object: " +  jsonUpdate["name"] +", confidence: " + jsonUpdate["confidence"])
            topicGuid = topicAnswer.json()["guid"]
            #create viewpoint
            viewPointAnswer = createBCFViewpoint(ACCESS_TOKEN, issue_board_id, topicGuid)
            viewpointGuid = viewPointAnswer.json()["guid"]
            #create second viewpoint
            viewPointAnswer2 = createBCFViewpoint(ACCESS_TOKEN, issue_board_id, topicGuid)
            viewpointGuid2 = viewPointAnswer2.json()["guid"]
            #create comment
            #createBCFComment(ACCESS_TOKEN, issue_board_id, topicGuid, json.loads(json.dumps(payload)), viewpointGuid)
            createBCFComment(ACCESS_TOKEN, issue_board_id, topicGuid, json.loads(payload), viewpointGuid)
            #upload snapshot
            uploadBCFSnapshot(ACCESS_TOKEN, issue_board_id, topicGuid, viewpointGuid, jsonUpdate["localOrigFileName"])
            uploadBCFSnapshot(ACCESS_TOKEN, issue_board_id, topicGuid, viewpointGuid2, jsonUpdate["localAnchorFileName"])




        except Exception as e:
            _logger.info("Error happened: "+ str(e))


    def options(self):
        self.set_status(204)
        self.finish()

application = tornado.web.Application([
    (r'/ImageToBCF', addImageData)
])


if __name__ == "__main__":
    _logger.info("Starting tornado server")
    application.listen(8084)
    tornado.ioloop.IOLoop.instance().start()
