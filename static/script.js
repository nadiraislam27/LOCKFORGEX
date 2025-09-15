// Slider display
const lengthSlider = document.getElementById('length');
const lengthValue = document.getElementById('lengthValue');
const output = document.getElementById('output');
const serviceInput = document.getElementById('serviceInput');

lengthSlider.oninput = () => {
  lengthValue.textContent = lengthSlider.value;
};

// Generate Password
function generatePassword() {
  const length = parseInt(lengthSlider.value);
  let chars = '';
  if (document.getElementById('uppercase').checked)
    chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  if (document.getElementById('lowercase').checked)
    chars += 'abcdefghijklmnopqrstuvwxyz';
  if (document.getElementById('numbers').checked) chars += '0123456789';
  if (document.getElementById('symbols').checked) chars += '!@#$%^&*()_+';

  if (!chars) return alert('⚠️ Select at least one character type.');

  let password = '';
  for (let i = 0; i < length; i++) {
    password += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  output.value = password;
}

// Copy generated password
function copyToClipboard() {
  if (!output.value) return alert('⚠️ Generate a password first!');
  navigator.clipboard
    .writeText(output.value)
    .then(() => alert('🔒 Password copied to clipboard!'))
    .catch(err => console.error('Copy failed', err));
}

// Save password with service
function savePassword() {
  const service = serviceInput.value.trim();
  const password = output.value;

  if (!service) return alert('⚠️ Enter the service name.');
  if (!password) return alert('⚠️ Generate a password first!');

  fetch('/save_password', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `service=${encodeURIComponent(service)}&password=${encodeURIComponent(
      password
    )}`,
  })
    .then(() => {
      alert('✅ Password saved successfully!');

      // Show password memory tip
      alert(
        '💡 Tip to remember your password:\n' +
          '1. Associate it with the service name.\n' +
          '2. Break it into chunks or a memorable phrase.\n' +
          '3. Visualize typing it on the keyboard.\n' +
          '4. Create a rhyme or story using symbols and numbers.'
      );

      serviceInput.value = '';
      output.value = '';
      location.reload(); // Refresh table to show new password
    })
    .catch(err => console.error('Save failed', err));
}

// Copy saved password from table
function copySavedPassword(password) {
  navigator.clipboard
    .writeText(password)
    .then(() => alert('🔒 Password copied to clipboard!'))
    .catch(err => console.error('Copy failed', err));
}
