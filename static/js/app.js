document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const pdfInput = document.getElementById('pdfInput');
    const fileName = document.getElementById('fileName');
    const uploadBtn = document.getElementById('uploadBtn');

    const uploadSection = document.getElementById('uploadSection');
    const loadingSection = document.getElementById('loadingSection');
    const resultsSection = document.getElementById('resultsSection');
    const errorSection = document.getElementById('errorSection');

    // Update file name when file is selected
    pdfInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            fileName.textContent = e.target.files[0].name;
        } else {
            fileName.textContent = 'Choose PDF file...';
        }
    });

    // Handle form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const file = pdfInput.files[0];
        if (!file) {
            showError('Please select a PDF file');
            return;
        }

        if (file.type !== 'application/pdf') {
            showError('Please select a valid PDF file');
            return;
        }

        // Show loading state
        uploadSection.style.display = 'none';
        loadingSection.style.display = 'block';
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';

        // Prepare form data
        const formData = new FormData();
        formData.append('pdf', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok && data.success) {
                displayResults(data);
            } else {
                showError(data.error || 'An error occurred while processing the PDF');
            }
        } catch (error) {
            showError('Network error: ' + error.message);
        }
    });
});

function displayResults(data) {
    // Hide loading, show results
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';

    // Set document name
    document.getElementById('documentName').textContent = data.filename;

    // Set summary
    document.getElementById('summaryContent').textContent = data.summary;

    // Set takeaways
    const takeawaysContainer = document.getElementById('takeawaysContent');
    takeawaysContainer.innerHTML = '';

    data.takeaways.forEach((takeaway, index) => {
        const takeawayDiv = document.createElement('div');
        takeawayDiv.className = 'takeaway-item';

        const takeawayText = document.createElement('p');
        takeawayText.textContent = takeaway;
        takeawayDiv.appendChild(takeawayText);

        takeawaysContainer.appendChild(takeawayDiv);
    });

    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
}

function resetAnalysis() {
    // Reset form
    document.getElementById('uploadForm').reset();
    document.getElementById('fileName').textContent = 'Choose PDF file...';

    // Show upload section
    document.getElementById('uploadSection').style.display = 'block';
    document.getElementById('loadingSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
