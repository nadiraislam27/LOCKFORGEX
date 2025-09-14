const lengthSlider = document.getElementById('length');
const lengthValue = document.getElementById('lengthValue');
const output = document.getElementById('output');

lengthSlider.oninput = () => {
  lengthValue.textContent = lengthSlider.value;
};

function generatePassword() {
  const length = parseInt(lengthSlider.value);
  const chars =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+';
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
