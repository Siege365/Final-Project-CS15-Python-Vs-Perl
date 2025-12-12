/**
 * Account Management
 * Handles profile updates, password changes, and eye icon toggle
 */

document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility - Fixed
    document.querySelectorAll('.toggle-password').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.dataset.target;
            const input = document.getElementById(targetId);
            const eyeOpen = this.querySelector('.eye-open');
            const eyeClosed = this.querySelector('.eye-closed');

            if (input.type === 'password') {
                input.type = 'text';
                eyeOpen.style.display = 'none';
                eyeClosed.style.display = 'block';
            } else {
                input.type = 'password';
                eyeOpen.style.display = 'block';
                eyeClosed.style.display = 'none';
            }
        });
    });

    // Profile form modal handling
    const profileForm = document.getElementById('profile-form');
    const profileModal = document.getElementById('profile-modal');
    const profileModalClose = document.getElementById('profile-modal-close');
    const profileCancel = document.getElementById('profile-cancel');
    const profileConfirm = document.getElementById('profile-confirm');
    let profileSubmitting = false;

    function closeProfileModal() {
        profileModal.classList.remove('show');
    }

    profileModalClose.addEventListener('click', closeProfileModal);
    profileCancel.addEventListener('click', closeProfileModal);
    profileModal.querySelector('.modal-backdrop').addEventListener('click', closeProfileModal);

    profileForm.addEventListener('submit', function(e) {
        if (!profileSubmitting) {
            e.preventDefault();
            profileModal.classList.add('show');
        }
    });

    profileConfirm.addEventListener('click', function() {
        profileSubmitting = true;
        const submitBtn = profileForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-small"></span> Saving...';
        closeProfileModal();
        
        // Submit via AJAX for better UX
        fetch(profileForm.getAttribute('action'), {
            method: 'POST',
            body: new FormData(profileForm),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg> Save Changes';
            profileSubmitting = false;
            
            if (data.success) {
                showToast('Profile updated successfully!', 'success');
            } else {
                showToast(data.message || 'Failed to update profile', 'error');
            }
        })
        .catch(error => {
            console.error('Profile update error:', error);
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path><polyline points="17 21 17 13 7 13 7 21"></polyline><polyline points="7 3 7 8 15 8"></polyline></svg> Save Changes';
            profileSubmitting = false;
            showToast('An error occurred while saving profile', 'error');
        });
    });

    // Password form modal handling
    const passwordForm = document.getElementById('password-form');
    const passwordModal = document.getElementById('password-modal');
    const passwordModalClose = document.getElementById('password-modal-close');
    const passwordCancel = document.getElementById('password-cancel');
    const passwordConfirm = document.getElementById('password-confirm');
    let passwordSubmitting = false;

    function closePasswordModal() {
        passwordModal.classList.remove('show');
    }

    passwordModalClose.addEventListener('click', closePasswordModal);
    passwordCancel.addEventListener('click', closePasswordModal);
    passwordModal.querySelector('.modal-backdrop').addEventListener('click', closePasswordModal);

    passwordForm.addEventListener('submit', function(e) {
        if (!passwordSubmitting) {
            e.preventDefault();
            
            // Validate passwords match
            const newPassword = document.getElementById('new_password').value;
            const confirmPassword = document.getElementById('confirm_password').value;

            if (newPassword !== confirmPassword) {
                showToast('Passwords do not match', 'error');
                return false;
            }
            
            if (newPassword.length < 6) {
                showToast('Password must be at least 6 characters', 'error');
                return false;
            }
            
            passwordModal.classList.add('show');
        }
    });

    passwordConfirm.addEventListener('click', function() {
        passwordSubmitting = true;
        const submitBtn = passwordForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-small"></span> Updating...';
        closePasswordModal();
        
        // Submit password form
        fetch(passwordForm.getAttribute('action'), {
            method: 'POST',
            body: new FormData(passwordForm),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg> Update Password';
            passwordSubmitting = false;
            
            if (data.success) {
                showToast('Password updated successfully!', 'success');
                passwordForm.reset();
            } else {
                showToast(data.message || 'Failed to update password', 'error');
            }
        })
        .catch(error => {
            console.error('Password update error:', error);
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg> Update Password';
            passwordSubmitting = false;
            showToast('An error occurred while updating password', 'error');
        });
    });
});
