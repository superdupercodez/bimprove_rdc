#!/bin/bash
curl -iX POST \
'http://localhost:8084/fusekiAddImage' \
-H 'Content-Type: text/plain' \
-d '{"imageID": "2MppzXLWeT", "name":"Safetynet", "confidence": "0.44544", "xmax": "675.44312", "xmin": "345.86625", "ymax": "876.31249", "ymin": "436.5287", "imageURL": "https://bit.ly/3glwtiH", "anchorBoxImageURL": "https://bit.ly/3glwtiH"}'
