// Verocta Financial Insight Platform - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initializeFeatherIcons();
    initializeFileUpload();
    initializeAnimations();
    initializeTooltips();
    
    console.log('Verocta Financial Platform initialized');
});

// Initialize Feather Icons with fallback handling
function initializeFeatherIcons() {
    if (typeof feather !== 'undefined') {
        try {
            feather.replace();
        } catch (error) {
            console.warn('Some feather icons may not be available:', error.message);
        }
    }
}

// File Upload Handling with Enhanced Drag & Drop and Logo Support
function initializeFileUpload() {
    const dropArea = document.getElementById('fileDropArea');
    const fileInput = document.getElementById('file');
    const logoInput = document.getElementById('companyLogo');
    const filePreview = document.getElementById('filePreview');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const removeFileBtn = document.getElementById('removeFile');
    const uploadForm = document.getElementById('uploadForm');

    // Enhanced drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    dropArea.addEventListener('drop', handleDrop, false);
    dropArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelection);
    logoInput.addEventListener('change', handleLogoSelection);
    removeFileBtn.addEventListener('click', clearFileSelection);
    uploadForm.addEventListener('submit', handleFormSubmission);
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    const dropArea = document.getElementById('fileDropArea');
    dropArea.classList.add('dragover');
}

function unhighlight(e) {
    const dropArea = document.getElementById('fileDropArea');
    dropArea.classList.remove('dragover');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        const file = files[0];
        if (file.type === 'text/csv' || file.name.toLowerCase().endsWith('.csv')) {
            document.getElementById('file').files = files;
            showFilePreview(file);
        } else {
            showNotification('Please drop a CSV file', 'warning');
        }
    }
}

function handleFileSelection(event) {
    const file = event.target.files[0];
    if (file) {
        showFilePreview(file);
    }
}

function handleLogoSelection(event) {
    const file = event.target.files[0];
    if (file) {
        // Validate logo file type
        const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/svg+xml'];
        if (!allowedTypes.includes(file.type)) {
            showNotification('Please select a PNG, JPG, JPEG, or SVG file for the logo', 'warning');
            event.target.value = '';
            return;
        }
        
        // Validate file size (2MB max)
        if (file.size > 2 * 1024 * 1024) {
            showNotification('Logo file size must be less than 2MB', 'warning');
            event.target.value = '';
            return;
        }
        
        showNotification(`Logo selected: ${file.name}`, 'success');
    }
}

function showFilePreview(file) {
    const filePreview = document.getElementById('filePreview');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const dropArea = document.getElementById('fileDropArea');
    
    fileName.textContent = file.name;
    fileSize.textContent = `(${formatFileSize(file.size)})`;
    
    filePreview.classList.remove('d-none');
    dropArea.style.display = 'none';
    
    // Re-initialize feather icons for the preview
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function clearFileSelection() {
    const fileInput = document.getElementById('file');
    const filePreview = document.getElementById('filePreview');
    const dropArea = document.getElementById('fileDropArea');
    
    fileInput.value = '';
    filePreview.classList.add('d-none');
    dropArea.style.display = 'block';
}

function handleFormSubmission(event) {
    event.preventDefault();
    
    const fileInput = document.getElementById('file');
    const uploadBtn = document.getElementById('uploadBtn');
    const btnText = uploadBtn.querySelector('.btn-text');
    const btnLoading = uploadBtn.querySelector('.btn-loading');
    
    if (!fileInput.files || fileInput.files.length === 0) {
        showNotification('Please select a CSV file', 'warning');
        return;
    }
    
    // Show loading state
    btnText.classList.add('d-none');
    btnLoading.classList.remove('d-none');
    uploadBtn.disabled = true;
    
    // Submit the form
    event.target.submit();
}

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    document.getElementById('fileDropArea').classList.add('dragover');
}

function unhighlight(e) {
    document.getElementById('fileDropArea').classList.remove('dragover');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length > 0) {
        const fileInput = document.getElementById('file');
        fileInput.files = files;
        handleFileSelection({ target: fileInput });
    }
}

function handleFileSelection(event) {
    const file = event.target.files[0];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (file) {
        // Validate file size
        if (file.size > maxSize) {
            showAlert('File size must be less than 16MB', 'error');
            clearFileSelection();
            return;
        }
        
        // Validate file type
        if (!file.name.toLowerCase().endsWith('.csv')) {
            showAlert('Please select a CSV file', 'error');
            clearFileSelection();
            return;
        }
        
        // Show file preview
        showFilePreview(file);
        
        console.log('File selected:', file.name, formatFileSize(file.size));
    }
}

function showFilePreview(file) {
    const dropArea = document.getElementById('fileDropArea');
    const filePreview = document.getElementById('filePreview');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    
    if (dropArea && filePreview && fileName && fileSize) {
        // Hide drop area and show preview
        dropArea.classList.add('d-none');
        filePreview.classList.remove('d-none');
        
        // Update preview content
        fileName.textContent = file.name;
        fileSize.textContent = `(${formatFileSize(file.size)})`;
        
        // Re-initialize icons
        feather.replace();
    }
}

function clearFileSelection() {
    const fileInput = document.getElementById('file');
    const dropArea = document.getElementById('fileDropArea');
    const filePreview = document.getElementById('filePreview');
    
    if (fileInput) {
        fileInput.value = '';
    }
    
    if (dropArea && filePreview) {
        dropArea.classList.remove('d-none');
        filePreview.classList.add('d-none');
    }
}

function handleFormSubmission(event) {
    const submitBtn = event.target.querySelector('button[type="submit"]');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoading = submitBtn.querySelector('.btn-loading');
    
    if (submitBtn && btnText && btnLoading) {
        // Show loading state
        submitBtn.disabled = true;
        btnText.classList.add('d-none');
        btnLoading.classList.remove('d-none');
        
        // Add progress tracking
        trackUploadProgress();
    }
}

function trackUploadProgress() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 95) {
            clearInterval(interval);
            progress = 95;
        }
        
        // Update progress if progress bar exists
        const progressBar = document.querySelector('.upload-progress');
        if (progressBar) {
            progressBar.style.width = progress + '%';
        }
    }, 500);
}

// Animation Handling
function initializeAnimations() {
    // Animate score circle if present
    const scoreCircle = document.querySelector('.score-circle');
    if (scoreCircle) {
        setTimeout(() => {
            scoreCircle.classList.add('animate');
        }, 500);
    }
    
    // Fade in cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe cards for animation
    document.querySelectorAll('.feature-card, .metric-card, .recommendation-item').forEach(card => {
        observer.observe(card);
    });
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Utility Functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        <i data-feather="${type === 'error' ? 'alert-circle' : 'info'}" class="me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of main content
    const main = document.querySelector('main');
    if (main) {
        main.insertBefore(alertContainer, main.firstChild);
        feather.replace();
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertContainer && alertContainer.parentNode) {
                alertContainer.remove();
            }
        }, 5000);
    }
}

// Download handling
function handleDownload(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Copy to clipboard functionality
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Copied to clipboard!', 'success');
        }).catch(() => {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showAlert('Copied to clipboard!', 'success');
    } catch (err) {
        showAlert('Failed to copy to clipboard', 'error');
    }
    
    document.body.removeChild(textArea);
}

// Score animation
function animateScore(element, targetScore, duration = 2000) {
    const startScore = 0;
    const startTime = performance.now();
    
    function updateScore(timestamp) {
        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function
        const easedProgress = 1 - Math.pow(1 - progress, 3);
        const currentScore = startScore + (targetScore - startScore) * easedProgress;
        
        element.textContent = Math.round(currentScore * 10) / 10;
        
        if (progress < 1) {
            requestAnimationFrame(updateScore);
        }
    }
    
    requestAnimationFrame(updateScore);
}

// Format currency
function formatCurrency(amount, currency = 'USD') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2
    }).format(amount);
}

// Format percentage
function formatPercentage(value, decimals = 1) {
    return (value).toFixed(decimals) + '%';
}

// Debounce function for search/filter inputs
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Theme handling (if needed in future)
function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('verocta-theme', theme);
}

function getTheme() {
    return localStorage.getItem('verocta-theme') || 'light';
}

// Enhanced notification system
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 500px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Enhanced form validation
function validateForm() {
    const fileInput = document.getElementById('file');
    const companyName = document.getElementById('companyName');
    const logoInput = document.getElementById('companyLogo');
    
    let isValid = true;
    
    // Validate CSV file
    if (!fileInput.files || fileInput.files.length === 0) {
        showNotification('Please select a CSV file', 'warning');
        isValid = false;
    } else {
        const file = fileInput.files[0];
        if (!file.name.toLowerCase().endsWith('.csv')) {
            showNotification('Please select a valid CSV file', 'warning');
            isValid = false;
        }
        if (file.size > 16 * 1024 * 1024) { // 16MB limit
            showNotification('File size must be less than 16MB', 'warning');
            isValid = false;
        }
    }
    
    // Validate logo if provided
    if (logoInput && logoInput.files && logoInput.files.length > 0) {
        const logoFile = logoInput.files[0];
        const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/svg+xml'];
        if (!allowedTypes.includes(logoFile.type)) {
            showNotification('Logo must be PNG, JPG, JPEG, or SVG format', 'warning');
            isValid = false;
        }
        if (logoFile.size > 2 * 1024 * 1024) { // 2MB limit for logos
            showNotification('Logo file size must be less than 2MB', 'warning');
            isValid = false;
        }
    }
    
    // Validate company name length
    if (companyName && companyName.value && companyName.value.length > 100) {
        showNotification('Company name must be less than 100 characters', 'warning');
        isValid = false;
    }
    
    return isValid;
}

// Error handling
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    
    // Don't show error alerts for minor issues
    if (event.error && event.error.message && 
        !event.error.message.includes('feather') && 
        !event.error.message.includes('bootstrap')) {
        showNotification('An unexpected error occurred. Please refresh the page.', 'error');
    }
});

// Performance monitoring
if ('performance' in window && 'mark' in performance) {
    performance.mark('verocta-js-loaded');
}

// Export functions for use in other scripts
window.VeroctaUtils = {
    showAlert,
    showNotification,
    validateForm,
    formatFileSize,
    formatCurrency,
    formatPercentage,
    copyToClipboard,
    animateScore,
    debounce
};
