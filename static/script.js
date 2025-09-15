const lengthSlider = document.getElementById('length');
const lengthValue = document.getElementById('lengthValue');
const output = document.getElementById('output');
const typeSelect = document.getElementById('type');
const tipPopup = document.getElementById('tipPopup');
const tipText = document.getElementById('tipText');

lengthSlider.oninput = () => {
  lengthValue.textContent = lengthSlider.value;
};

function generatePassword() {
  const length = parseInt(lengthSlider.value);
  let chars = '';

  switch (typeSelect.value) {
    case 'upper':
      chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
      break;
    case 'lower':
      chars = 'abcdefghijklmnopqrstuvwxyz';
      break;
    case 'number':
      chars = '0123456789';
      break;
    default:
      chars =
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+';
  }

  let password = '';
  for (let i = 0; i < length; i++) {
    password += chars.charAt(Math.floor(Math.random() * chars.length));
  }

  output.value = password;
}

function copyToClipboard() {
  if (!output.value) return alert('⚠️ Generate a password first!');
  navigator.clipboard
    .writeText(output.value)
    .then(() => alert('🔒 Password copied to clipboard!'))
    .catch(err => console.error('Copy failed', err));
}

// Copy saved password
function copySavedPassword(password) {
  navigator.clipboard
    .writeText(password)
    .then(() => alert('🔒 Saved password copied!'))
    .catch(err => console.error('Copy failed', err));
}

// Save password with service name
function savePassword() {
  const service = document.getElementById('service').value;
  const password = output.value;

  if (!service || !password) {
    return alert('⚠️ Please enter a service and generate a password first.');
  }

  fetch('/save_password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `service=${encodeURIComponent(service)}&password=${encodeURIComponent(
      password
    )}`,
  })
    .then(res => res.json())
    .then(data => {
      if (data.message) {
        showTip(service, password);
        // Add to list dynamically
        const ul = document.getElementById('savedPasswords');
        const li = document.createElement('li');
        li.innerHTML = `<strong>${service}:</strong> ${password} <button onclick="copySavedPassword('${password}')">Copy</button>`;
        ul.appendChild(li);
      }
    });
}

// Show memory tip
function showTip(service, password) {
  tipText.textContent = `💡 Tip: To remember the password for ${service}, create a story or pattern using parts of it!`;
  tipPopup.style.display = 'block';
}

// Close tip popup
function closeTip() {
  tipPopup.style.display = 'none';
}
