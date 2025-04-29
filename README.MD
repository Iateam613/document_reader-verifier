# Document Reader & Verifier

This project is a **Django-based web application** designed to process, extract, and verify information from uploaded document images. It leverages **OpenAI's GPT model** for Optical Character Recognition (OCR) and text analysis, providing high-precision field detection, verbatim extraction, and verification of document authenticity.

---

## Features

- **File Upload**: Users can upload document images (e.g., PNG, JPEG , PDF).
- **OCR Processing**: Extracts text fields and their values from the uploaded document.
- **Field Verification**: Verifies the authenticity and correctness of the extracted fields.
- **Error Handling**: Graceful handling of invalid files or processing errors.
- **Frontend Integration**: Provides a drag-and-drop interface for file uploads and displays results dynamically.

---

## Project Structure

### **1. `reader_app`**
This is the core Django app that handles file uploads, processing, and verification.

#### Key Files:
- **`views.py`**:
  - Handles file uploads via the `reader` view.
  - Saves uploaded files temporarily, processes them using utility functions, and returns JSON responses.
  - Deletes temporary files after processing.
  
- **`utils.py`**:
  - Contains utility functions:
    - `process_details(image_path)`: Extracts text fields and their values from the document image using OpenAI's GPT model.
    - `get_verification(image_path)`: Verifies the authenticity of the document.
  - Handles base64 encoding of images and OpenAI API calls.

- **`static/js/script.js`**:
  - Provides frontend functionality:
    - Drag-and-drop file upload.
    - Displays a preview of the uploaded image.
    - Sends files to the backend for processing.
    - Displays extracted details and verification results dynamically.

- **`templates/index.html`**:
  - The main HTML template for the application.
  - Includes the file upload interface and placeholders for displaying results.

---

### **2. `document_reader`**
This is the main Django project directory.

#### Key Files:
- **`settings.py`**:
  - Configures installed apps, middleware, and templates.
  - Includes the `reader_app` as a custom app.
  - Defines the `MEDIA_ROOT` for handling uploaded files.

- **`urls.py`**:
  - Maps URLs to views in the `reader_app`.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Django 4.x
- OpenAI Python SDK
- Node.js (for frontend development, optional)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/Iateam613/document_reader-verifier.git
   cd document_reader-verifier
