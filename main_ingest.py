
import os
import time
import json
import magic

from processors.process_audio import process_audio, process_transcript
from processors.process_image import process_image
from processors.process_pdf import process_pdf
from processors.process_excel import process_excel
from processors.process_word import process_word
from processors.process_ppt import process_ppt
from processors.process_text import process_text
from processors.content_processing import content_processing
from db_support.process_db_support import insert_row


class FileProcessor:
    def __init__(self, file_path):
        print(file_path)
        # Check if the path is a file
        if os.path.isdir(file_path):
            raise IsADirectoryError(f"Expected a file but got a directory: {file_path}")
        self.file_path = file_path
        self.file_metadata = {
            'file_name': os.path.basename(file_path),
            'file_extension': os.path.splitext(file_path)[1].lower(),
            'file_path': file_path,
            'file_size': os.path.getsize(file_path),
            'file_creation_time': time.ctime(os.path.getctime(file_path)),
            'file_modification_time': time.ctime(os.path.getmtime(file_path)),
            'file_accessed_time': time.ctime(os.path.getatime(file_path)),
            'file_mime_type': magic.from_file(file_path, mime=True)  # Get MIME type
        }
        self.application_metadata = {}  # Section for application-specific metadata
        self.extracted_content = {}
        self.content_data = {}
        self.usage_data = {}
        self.security_policy = {}
        self.retention_policy= {}
        self.destruction_policy= {}

    def process_file(self):
        # Group extensions to determine the file type
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
        video_extensions = ['.mp4', '.avi', '.mkv', '.mov']
        audio_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.aiff', '.opus', '.asf', '.alac']
        text_extensions = ['.txt', '.md', '.log']
        csv_extensions = ['.csv', '.tsv']
        json_extensions = ['.json']
        pdf_extensions = ['.pdf']
        ms_excel_extensions = ['.xls', '.xlsx', '.xlsb']
        ms_word_extensions = ['.doc', '.docx']
        ms_powerpoint_extensions = ['.ppt', '.pptx']
        database_extensions = ['.db', '.sqlite', '.db', '.sqlite3', '.mdb']
        zip_extensions = ['.zip', '.rar', '.tar', '.gz']
        backup_extensions = ['.bak', '.backup', '.backups', '.iso', '.vhd', '.vmdk'] # iso = disk image, vhd/vmdk = virtual machine disk files
        email_extensions = ['.eml', '.pst', '.ost', '.edb'] # ebd = exchange db
        design_extensions = ['.psd', '.dwg'] # psd = photoshop and dwg = autocad
        vm_extensions = ['.vm', '.vmx', '.vmdk', '.vhdx']
        security_extensions = ['.key', '.keytab', '.crypto', '.cer', '.crt']
        license_extensions = ['.lic', '.cfg']
        analytics_extensions = ['.pbix', 'qvf', '.twbx'] # powerBI, qlik and tableau
        system_extensions = ['.sys', '.cmd', '.cmdx', '.dll', '.exe', '.dmg']
        development_extensions = ['.java', '.py', '.js', '.html', '.json', '.git']

        # Check the file extension and call the respective processing method
        if self.file_metadata['file_extension'] in image_extensions:
            #self.application_metadata.update(process_image(self.file_path))
            # Update application metadata with the processed image data
            extracted_content = process_image(self.file_path)
            # Add color and image summary to application metadata
            self.application_metadata.update({
                'colors': extracted_content['colors'],
                'image_summary': extracted_content['image_summary']
            })
        elif self.file_metadata['file_extension'] in text_extensions:
            self.application_metadata.update(process_text(self.file_path))
#        elif self.file_metadata['file_extension'] in csv_extensions:
#            self.application_metadata.update(process_csv(self.file_path))
#        elif self.file_metadata['file_extension'] in json_extensions:
#            self.application_metadata.update(process_json(self.file_path))
        elif self.file_metadata['file_extension'] in pdf_extensions:
            self.application_metadata.update(process_pdf(self.file_path))
        elif self.file_metadata['file_extension'] in ms_excel_extensions:
            self.application_metadata.update(process_excel(self.file_path))
        elif self.file_metadata['file_extension'] in ms_word_extensions:
            metadata, body_text = process_word(self.file_path)  # Unpack the tuple
            self.application_metadata.update(metadata)  # Update the application metadata with the metadata part
            self.extracted_content = body_text  # Store the extracted body text separately
            # After extracting the content, call content_processing to analyze the text
            if self.extracted_content:
                self.content_data = content_processing(self.extracted_content['body_text'])
        elif self.file_metadata['file_extension'] in ms_powerpoint_extensions:
            self.application_metadata.update(process_ppt(self.file_path))
        elif self.file_metadata['file_extension'] in audio_extensions:
            audio_data = process_audio(self.file_path)
            extracted_content = process_transcript(self.file_path)
            if 'metadata' in audio_data:
                self.application_metadata.update(audio_data['metadata'])
            # Check if 'transcript' exists and update transcript data
            if 'transcript' in extracted_content:
                self.extracted_content.update({'transcript': extracted_content['transcript']})
            else:
                self.extracted_content.update({'transcript': 'No transcript available'})
        else:
            self.application_metadata['status'] = 'Unsupported file type'

    def get_file_data(self):
        # Return all gathered metadata in sections
        return {
            'file_metadata': self.file_metadata,
            'application_metadata': self.application_metadata,
            'extracted_content': self.extracted_content,
            'content_data': self.content_data,
            'security_policy': self.security_policy,
            'retention_policy': self.retention_policy,
            'destruction_policy': self.destruction_policy
        }


# Example usage

file_path = '/datadrive/Assets/Gator/GatorBait/rankings.xlsx'
# Process each file and print its metadata
#for file_path in file_paths:
print(file_path)
processor = FileProcessor(file_path)
processor.process_file()
metadata = processor.get_file_data()
row_data = {
    'file_name': metadata['file_metadata']['file_name'],
    'file_size': metadata['file_metadata']['file_size'],
    'file_type': metadata['file_metadata']['file_extension'],
    'additional_data': metadata['application_metadata']['sheet_names']
}
print(row_data)
row_data['additional_data'] = json.dumps(row_data['additional_data'])
insert_row('/home/rbump/savartus_dlm/config.json', 'processed_files', row_data)
    #print(json.dumps(metadata, indent=4))
print(metadata)


##########################

#image_summary('/Users/rickbump/Library/Mobile Documents/com~apple~CloudDocs/Personal/19011 Highview Court/2018 remodel/IMG_0006.jpeg')
# Example usage
#colors, percentages = summarize_colors('/Users/rickbump/Library/Mobile Documents/com~apple~CloudDocs/Personal/19011 Highview Court/2018 remodel/IMG_0006.jpeg', num_colors=5)
#print("Dominant Colors: ", colors)
#print("Percentages: ", percentages)
# Example usage
#colors, percentages = summarize_colors('http://images.cocodataset.org/val2017/000000039769.jpg', num_colors=5)
# Plot and save the pie chart
#plot_and_save_pie_chart(colors, percentages, save_path='color_pie_chart.png')