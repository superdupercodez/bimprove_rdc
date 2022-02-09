"""Perform test request"""
import pprint

import requests

DETECTION_URL = "http://localhost:5001/v1/risk_objects/"
TEST_IMAGE = "madrid_test_image.jpg"

image_data = open(TEST_IMAGE, "rb").read()

response = requests.post(DETECTION_URL, files={"image": image_data}).json()

pprint.pprint(response)
