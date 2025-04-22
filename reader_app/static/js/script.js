const uploadBox       = document.getElementById('uploadBox');
const fileInput       = document.getElementById('fileInput');
const processBtn      = document.getElementById('processBtn');
const descriptionBox  = document.getElementById('description');
const verificationBox = document.getElementById('verification');
const loadingModal    = document.getElementById('loadingModal');
const loadingMessage  = document.getElementById('loadingMessage');

let selectedFiles = [];

// 1) Select files
uploadBox.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', e => {
  selectedFiles = Array.from(e.target.files);
  uploadBox.innerHTML = `<p><strong>${selectedFiles.length} file(s) selected</strong></p>`;
});

// 2) Show/hide loading modal
function showLoading(msg) {
  loadingMessage.textContent = msg;
  loadingModal.classList.remove('hidden');
}
function hideLoading() {
  loadingModal.classList.add('hidden');
}

// 3) Render the returned data array
function displayData(results) {
  console.log('displayData got:', results);
  results.forEach((r, i) => {
    console.log(
      `#${i}`, 
      'details=', r.details, 
      'verification=', r.verification
    );
  });

  // fall back to any “detail” key if “details” is missing:
  const allDetails = results
    .map(r => r.details ?? r.detail ?? '')
    .join('\n\n');

  const allVerifications = results
    .map(r => r.verification ?? r.verify ?? '')
    .join('\n\n');

  descriptionBox.value  = allDetails       || 'No details returned.';
  verificationBox.value = allVerifications || 'No verification returned.';
}


// 4) Send files to Django and handle JSON response
processBtn.addEventListener('click', async () => {
  if (!selectedFiles.length) {
    return alert('Please upload at least one file.');
  }

  showLoading('AI File verification ongoing, please wait…');

  const formData = new FormData();
  selectedFiles.forEach(f => formData.append('files', f));

  try {
    const response = await fetch('/verify/', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error(`Server error ${response.status}:`, errText);
      throw new Error(`Server responded ${response.status}`);
    }

    const data = await response.json();
    console.log('Parsed JSON:', data);

    if (Array.isArray(data.results) && data.results.length) {
      displayData(data.results);
    } else if (data.error) {
      alert(data.error);
    } else {
      displayData([]);
    }

  } catch (err) {
    console.error('Processing error:', err);
    alert('Error processing the file(s). Check console for details.');
  } finally {
    hideLoading();
  }
});

