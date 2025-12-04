import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import PyPDF2
import anthropic
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        raise Exception(f"Error extracting PDF text: {str(e)}")
    return text

def generate_summary(pdf_text):
    """Generate summary and takeaways using Claude API"""
    try:
        # Get API key from environment variable
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            return {
                'summary': 'Error: ANTHROPIC_API_KEY not set in environment variables.',
                'takeaways': [
                    'Please set your Anthropic API key',
                    'Export ANTHROPIC_API_KEY=your_key_here',
                    'Then restart the application'
                ]
            }

        client = anthropic.Anthropic(api_key=api_key)

        prompt = f"""You are analyzing a document for a Strategic Innovation Advisor at a Forensic Science Institute.

Based on the following PDF content, provide:
1. A concise summary (2-3 paragraphs) highlighting the key points
2. The top 3 strategic takeaways specifically relevant to innovation in forensic science

Format your response as follows:
SUMMARY:
[Your summary here]

TAKEAWAYS:
1. [First takeaway]
2. [Second takeaway]
3. [Third takeaway]

PDF Content:
{pdf_text[:15000]}  # Limit to avoid token limits
"""

        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text

        # Parse the response
        parts = response_text.split('TAKEAWAYS:')
        summary = parts[0].replace('SUMMARY:', '').strip()

        takeaways_text = parts[1].strip() if len(parts) > 1 else ""
        takeaways = []
        for line in takeaways_text.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering
                takeaway = line.lstrip('0123456789.-) ').strip()
                if takeaway:
                    takeaways.append(takeaway)

        # Ensure we have exactly 3 takeaways
        while len(takeaways) < 3:
            takeaways.append("Additional analysis required")
        takeaways = takeaways[:3]

        return {
            'summary': summary,
            'takeaways': takeaways
        }

    except Exception as e:
        return {
            'summary': f'Error generating summary: {str(e)}',
            'takeaways': ['Error occurred', 'Please check API key', 'And try again']
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['pdf']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    try:
        # Save the file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extract text from PDF
        pdf_text = extract_text_from_pdf(filepath)

        if not pdf_text.strip():
            return jsonify({'error': 'No text could be extracted from the PDF'}), 400

        # Generate summary and takeaways
        analysis = generate_summary(pdf_text)

        # Clean up - optionally delete the file after processing
        # os.remove(filepath)

        return jsonify({
            'success': True,
            'filename': file.filename,
            'summary': analysis['summary'],
            'takeaways': analysis['takeaways']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
