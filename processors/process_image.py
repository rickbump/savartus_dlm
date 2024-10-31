from PIL import Image, ExifTags
import requests
from ultralytics import YOLO
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from io import BytesIO


def process_image(file_path):
    extracted_content = {}

    # Extract metadata from the image
    metadata = process_image_metadata(file_path)
    extracted_content['metadata'] = metadata

    # Summarize colors in the image and add to extracted_content
    colors, percentages = summarize_colors(file_path)
    extracted_content['colors'] = {
        'dominant_colors': colors,
        'percentages': percentages
    }

    try:
        # Generate image summary including YOLO inference
        yolo_results = image_summary(file_path)
        extracted_content['image_summary'] = {
            'yolo_results': yolo_results,
            'metadata': metadata
        }
    except Exception as e:
        # Handle cases where YOLO inference fails
        extracted_content['image_summary'] = f"Error generating image summary: {str(e)}"

    return extracted_content


def process_image_metadata(file_path):
    metadata = {}
    try:
        with Image.open(file_path) as image:
            metadata['image_width'], metadata['image_height'] = image.size
            metadata['image_format'] = image.format
            metadata['image_mode'] = image.mode

            # Extract EXIF data if available
            exif_data = image._getexif()
            if exif_data:
                exif = {}
                for tag, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag, tag)
                    exif[tag_name] = value
                metadata['exif'] = exif
            else:
                metadata['exif'] = 'No EXIF data found'
    except Exception as e:
        metadata['image_error'] = str(e)
    return metadata


def summarize_colors(image_path_or_url, num_colors=5):
    """Summarize the dominant colors in an image using KMeans clustering."""
    if image_path_or_url.startswith('http'):
        response = requests.get(image_path_or_url)
        image = Image.open(BytesIO(response.content))
        image = np.array(image)
    else:
        # Otherwise, read the image from a local path
        image = cv2.imread(image_path_or_url)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape the image to a list of pixels
    pixels = image.reshape(-1, 3)

    # Use KMeans to cluster the pixel colors
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(pixels)

    # Get the colors (cluster centers)
    colors = kmeans.cluster_centers_.astype(int)

    # Get the percentage of each color
    labels, counts = np.unique(kmeans.labels_, return_counts=True)
    percentages = counts / counts.sum()

    # Display the dominant colors with their percentages
    plt.figure(figsize=(8, 6))
    plt.pie(percentages, colors=[colors[i] / 255 for i in labels], labels=[f'Color {i + 1}' for i in labels])
    plt.show()

    return colors, percentages


def plot_and_save_pie_chart(colors, percentages, save_path='color_pie_chart.png'):
    # Plot the pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(percentages, colors=[colors[i] / 255 for i in range(len(colors))],
            labels=[f'Color {i + 1}' for i in range(len(colors))])
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is a circle.

    # Display the chart
    plt.show()

    # Save the chart to a file
    plt.savefig(save_path, bbox_inches='tight')
    print(f"Pie chart saved as {save_path}")


def image_summary(file_path):
    #source = 'http://images.cocodataset.org/val2017/000000039769.jpg'

    # •    'yolov8n.pt': Nano version(small and fast).
    # •    'yolov8s.pt': Small version(larger and slower but more accurate).
    # •    'yolov8m.pt': Medium version.
    # •    'yolov8l.pt': Large version.
    # •    'yolov8x.pt': Extra-large version.

    model = YOLO('yolov8x.pt')

    # Run inference on an image
    results = model(file_path)
    # print(results)
    # Print results or perform other processing
    results[0].show()  # Display the image with predictions
    return results
