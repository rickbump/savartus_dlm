import PyPDF2

def process_pdf(file_path):
    metadata = {}
    try:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            # Get document info (metadata)
            doc_info = pdf_reader.getDocumentInfo()
            metadata['pdf_page_count'] = pdf_reader.numPages

            if doc_info:
                # Print all available fields and values
                for key, value in doc_info.items():
                    metadata[key] = value
            else:
                metadata['error'] = 'No metadata found in the PDF'
    except Exception as e:
        metadata['error'] = str(e)

    return metadata