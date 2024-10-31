
#from ultralytics import YOLOv10
from ultralytics import YOLO

source = 'http://images.cocodataset.org/val2017/000000039769.jpg'

# •    'yolov8n.pt': Nano version(small and fast).
# •    'yolov8s.pt': Small version(larger and slower but more accurate).
# •    'yolov8m.pt': Medium version.
# •    'yolov8l.pt': Large version.
# •    'yolov8x.pt': Extra - large version.

model = YOLO('yolov8x.pt')

# Run inference on an image
results = model(source)
#print(results)
# Print results or perform other processing
results[0].show()  # Display the image with predictions