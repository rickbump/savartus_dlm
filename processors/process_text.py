import os
from charset_normalizer import from_path
import chardet
from processors.content_processing import content_processing

# Function to detect file encoding using chardet
def detect_encoding(file_path):
    try:
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']
            return {
                'encoding': encoding,
                'confidence': confidence
            }
    except Exception as e:
        return {'encoding_error': str(e)}

def process_text(file_path):
    try:
        # Detect file encoding first
        encoding_info = detect_encoding(file_path)  # or detect_encoding_charset_normalizer(file_path)
        encoding = encoding_info.get('encoding', 'utf-8')  # Default to utf-8 if detection fails

        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()

        text_metadata = {
            'character_count': len(content),
            'word_count': len(content.split()),
            'line_count': content.count('\n') + 1,
            'encoding': encoding_info  # Include encoding details
        }
        return text_metadata
    except Exception as e:
        return {'text_error': str(e)}