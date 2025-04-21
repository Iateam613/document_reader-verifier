const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const processBtn = document.getElementById('processBtn');
const descriptionBox = document.getElementById('description');
const verificationBox = document.getElementById('verification');
const loadingModal = document.getElementById('loadingModal');
const loadingMessage = document.getElementById('loadingMessage');

let selectedFiles = [];

// Open file dialog
uploadBox.addEventListener('click', () => fileInput.click());

// Show count of selected files
fileInput.addEventListener('change', (e) => {
  selectedFiles = e.target.files;
  uploadBox.innerHTML = `<p><strong>${selectedFiles.length} file(s) selected</strong></p>`;
});

// Show modal
function showLoading(message) {
  loadingMessage.textContent = message;
  loadingModal.classList.remove('hidden');
}

// Hide modal
function hideLoading() {
  loadingModal.classList.add('hidden');
}

// Process button click
processBtn.addEventListener('click', async () => {
  if (!selectedFiles.length) {
    alert('Please upload at least one file.');
    return;
  }

  // Show spinner with custom message
  showLoading('AI File verification ongoing, please wait...');

  const formData = new FormData();
  Array.from(selectedFiles).forEach(file => formData.append('files', file));

  try {
    const response = await fetch('/verify/', {
      method: 'POST',
      body: formData
    });
    const result = await response.json();

    descriptionBox.value = result.description || 'No description returned.';
    verificationBox.value = result.verification || 'No verification returned.';
  } catch (error) {
    console.error('Processing error:', error);
    alert('Error processing the files.');
  } finally {
    hideLoading();
  }
});