# PDF Strategic Analysis Web App

A web application that automatically generates AI-powered summaries and strategic takeaways from PDF documents, specifically tailored for Strategic Innovation Advisors in Forensic Science Institutes.

## Features

- **PDF Upload**: Drag-and-drop or click to upload PDF documents
- **AI-Powered Analysis**: Uses Claude AI to generate intelligent summaries
- **Strategic Takeaways**: Automatically extracts the top 3 key insights relevant to forensic science innovation
- **Beautiful UI**: Modern, responsive design that works on all devices
- **Print Support**: Generate printable reports of your analysis
- **Secure**: File size limits and type validation for security

## Prerequisites

- Python 3.8 or higher
- An Anthropic API key (get one at https://console.anthropic.com/)

## Installation

1. **Clone or navigate to the repository**
   ```bash
   cd SwiftPlayground
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Anthropic API key**

   On Linux/Mac:
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```

   On Windows:
   ```cmd
   set ANTHROPIC_API_KEY=your-api-key-here
   ```

   Or add it to your `.bashrc`, `.zshrc`, or environment variables permanently.

## Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**

   Navigate to: `http://localhost:5000`

3. **Upload a PDF**
   - Click "Choose PDF file" or drag and drop
   - Click "Analyze Document"
   - Wait for the AI analysis (typically 10-30 seconds)
   - View your summary and strategic takeaways!

## Usage

1. **Upload**: Select a PDF document (max 16MB)
2. **Analyze**: The app extracts text and sends it to Claude AI
3. **Review**: Get a comprehensive summary and 3 strategic takeaways
4. **Export**: Print or save the analysis for your records
5. **Repeat**: Analyze more documents as needed

## Project Structure

```
SwiftPlayground/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README_WEBAPP.md      # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Application styles
│   └── js/
│       └── app.js        # Frontend JavaScript
└── uploads/              # Uploaded PDFs (created automatically)
```

## How It Works

1. **Frontend**: User uploads a PDF through the web interface
2. **Backend**: Flask receives the file and extracts text using PyPDF2
3. **AI Processing**: Text is sent to Claude AI with a specialized prompt for forensic science analysis
4. **Response**: Claude generates a summary and 3 strategic takeaways
5. **Display**: Results are formatted and displayed in the web interface

## API Integration

This app uses the Anthropic Claude API (Sonnet 4.5 model) for intelligent document analysis. The AI is specifically prompted to:

- Understand the context of forensic science innovation
- Extract strategic insights relevant to advisors
- Provide actionable takeaways
- Summarize complex documents concisely

## Customization

### Modify the Analysis Prompt

Edit the prompt in `app.py` (line ~52) to customize the analysis style:

```python
prompt = f"""You are analyzing a document for a Strategic Innovation Advisor at a Forensic Science Institute.

Based on the following PDF content, provide:
1. A concise summary (2-3 paragraphs) highlighting the key points
2. The top 3 strategic takeaways specifically relevant to innovation in forensic science
...
```

### Change the Number of Takeaways

Modify the parsing logic in `app.py` to extract more or fewer takeaways.

### Adjust File Size Limits

Change the `MAX_CONTENT_LENGTH` in `app.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

## Troubleshooting

### "ANTHROPIC_API_KEY not set"
- Ensure you've exported the API key in your terminal session
- Restart the Flask app after setting the environment variable

### "No text could be extracted from the PDF"
- The PDF might be image-based (scanned). Try a text-based PDF
- The PDF might be corrupted or password-protected

### "Error generating summary"
- Check your internet connection
- Verify your API key is valid
- Ensure you have API credits remaining

## Security Notes

- PDFs are saved temporarily in the `uploads/` folder
- Consider implementing automatic file cleanup for production use
- The app runs on localhost by default (not exposed to the internet)
- For production deployment, use a proper WSGI server (gunicorn, uWSGI)

## Future Enhancements

- Support for multiple file formats (Word, text files)
- Batch processing of multiple PDFs
- User authentication and session management
- Database storage for analysis history
- Export to PDF/Word formats
- Comparison between multiple documents
- Custom analysis templates

## License

This project is provided as-is for educational and professional use.

## Support

For issues or questions about:
- **Claude API**: Visit https://docs.anthropic.com/
- **Flask**: Visit https://flask.palletsprojects.com/
- **This app**: Check the code comments or create an issue

---

**Built with**: Flask, Claude AI, PyPDF2, and modern web technologies
**Purpose**: Strategic analysis for forensic science innovation
