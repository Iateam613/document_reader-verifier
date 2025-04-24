const uploadBox       = document.getElementById('uploadBox');
const fileInput       = document.getElementById('fileInput');
const processBtn      = document.getElementById('processBtn');
const restartBtn      = document.getElementById('restartBtn');
const descriptionBox  = document.getElementById('description');
const verificationBox = document.getElementById('verification');
const loadingModal    = document.getElementById('loadingModal');
const loadingMessage  = document.getElementById('loadingMessage');
const previewContainer = document.getElementById('previewContainer');

let selectedFiles = [];

// Handle file selection or drop
function handleFile(file) {
  selectedFiles = [file];
  uploadBox.innerHTML = `<p><strong>${file.name} selected</strong></p>`;
  onUpload(file);
  displayPreview(file);
}

// Drag-and-drop events
['dragenter', 'dragover'].forEach(evt => {
  uploadBox.addEventListener(evt, e => {
    e.preventDefault();
    uploadBox.classList.add('drag-over');
  });
});

['dragleave', 'drop'].forEach(evt => {
  uploadBox.addEventListener(evt, e => {
    e.preventDefault();
    uploadBox.classList.remove('drag-over');
  });
});

uploadBox.addEventListener('drop', e => {
  const file = e.dataTransfer.files[0];
  if (file) handleFile(file);
});

// Click to select
uploadBox.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', e => {
  const file = e.target.files[0];
  if (file) handleFile(file);
});

// Display image preview
function displayPreview(file) {
  const reader = new FileReader();
  reader.onload = e => {
    previewContainer.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
  };
  reader.readAsDataURL(file);
}

// onUpload handler (provided by integration point)
function onUpload(file) {
  // Pass file to backend or further processing
  console.log('Uploading:', file);
}

// Restart state
restartBtn.addEventListener('click', () => {
  // Reset uploads
  selectedFiles = [];
  fileInput.value = '';
  uploadBox.innerHTML = `<p><strong>Upload PDF or Image</strong></p><p>+</p>`;
  // Clear outputs
  descriptionBox.value = '';
  verificationBox.value = '';
  // Clear preview
  previewContainer.innerHTML = '';
  // Hide loading if open
  loadingModal.classList.add('hidden');
});

// Loading modal
function showLoading(msg) {
  loadingMessage.textContent = msg;
  loadingModal.classList.remove('hidden');
}
function hideLoading() {
  loadingModal.classList.add('hidden');
}

// Process button
processBtn.addEventListener('click', async () => {
  if (!selectedFiles.length) return alert('Please upload at least one file.');
  showLoading('AI File verification ongoing, please wait…');

  const formData = new FormData();
  selectedFiles.forEach(f => formData.append('files', f));

  try {
    const response = await fetch('/verify/', { method: 'POST', body: formData });
    if (!response.ok) throw new Error(`Server responded ${response.status}`);
    const data = await response.json();
    if (Array.isArray(data.results) && data.results.length) displayData(data.results);
    else if (data.error) alert(data.error);
    else displayData([]);
  } catch (err) {
    console.error('Error:', err);
    alert('Error processing the file(s).');
  } finally {
    hideLoading();
  }
});

// Render returned data
function displayData(results) {
  const allDetails = results.map(r => r.details || r.detail || '').join('\n\n');
  const allVerifications = results.map(r => r.verification || r.verify || '').join('\n\n');
  descriptionBox.value  = allDetails || 'No details returned.';
  verificationBox.value = allVerifications || 'No verification returned.';
}

