/* ============================================================
   CCTV SYSTEM — main.js
   Shared JavaScript utilities for all pages
   ============================================================ */

/**
 * setupPasswordToggle
 * Attaches a show/hide toggle to a password input.
 *
 * @param {string} inputId   - The id of the <input type="password">
 * @param {string} toggleId  - The id of the <i> eye icon element
 */
function setupPasswordToggle(inputId, toggleId) {
  const input  = document.getElementById(inputId);
  const toggle = document.getElementById(toggleId);

  if (!input || !toggle) return;

  toggle.addEventListener('click', () => {
    if (input.type === 'password') {
      input.type = 'text';
      toggle.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
      input.type = 'password';
      toggle.classList.replace('fa-eye-slash', 'fa-eye');
    }
  });
}

/* ── Auto-init on DOMContentLoaded ──────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {

  /* Login page — single password field */
  setupPasswordToggle('password', 'togglePassword');

  /* Signup page — password + confirm password */
  setupPasswordToggle('password',        'togglePassword');
  setupPasswordToggle('confirmPassword', 'toggleConfirm');

});
