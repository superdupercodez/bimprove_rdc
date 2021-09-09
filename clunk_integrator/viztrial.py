from PIL import Image, ImageFont, ImageDraw

detections = [{'class': 0,
				'confidence': 0.3575510085,
				'name': 'barrier',
				'xmax': 2835.5417480469,
				'xmin': 582.5151367188,
				'ymax': 1872.4300537109,
				'ymin': 331.346862793}]

detections = []

img = Image.open('20.jpg')

width, height = img.size
font = ImageFont.truetype("Gidole-Regular.ttf", size=int(height/40))
for detection in detections:
    draw = ImageDraw.Draw(img)
    coords = ((detection['xmin'], detection['ymin']), (detection['xmax'], detection['ymax']))
    draw.rectangle(coords, outline ="yellow", width=30)

    label_text = detection['name'] + ' conf:' + str(detection['confidence'])
    label_box = draw.textsize(label_text, font)
    draw.rectangle(((coords[0][0], coords[0][1]),(coords[0][0] + label_box[0] +5, coords[0][1] + label_box[1] + 5)), outline="yellow", fill="yellow", width=10)
    draw.text(coords[0], label_text, (0,0,0), font=font)