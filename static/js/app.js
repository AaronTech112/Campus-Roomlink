// RoomLink MVP - Vanilla JS
// Refactored for Django Multi-Page App

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    // Initialize any interactive components that don't depend on data loading
    // e.g. check for toast messages in DOM and auto-hide them
    
    const toast = document.querySelector('.toast.show');
    if (toast) {
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }
});

// --- Modals ---

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('open');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('open');
        document.body.style.overflow = '';
    }
}

// --- Toast Logic (Callable from JS if needed) ---

function showToast(message) {
    const toast = document.getElementById('toast');
    if (toast) {
        toast.innerText = message;
        toast.classList.add('show');
        toast.classList.remove('hidden');
        
        setTimeout(() => {
            toast.classList.remove('show');
            // optionally add hidden back after transition
        }, 3000);
    }
}

// --- Form Interaction (Progressive Enhancement) ---
// If we wanted to add client-side validation or preview before submitting to Django

const postForm = document.querySelector('form[action*="post_listing"]');
if (postForm) {
    postForm.addEventListener('submit', (e) => {
        // Optional: Simple client-side check or loading state
        const btn = postForm.querySelector('button[type="submit"]');
        if (btn) {
            btn.innerText = 'Posting...';
            btn.disabled = true;
        }
        // Allow form to submit normally to Django
    });
}
