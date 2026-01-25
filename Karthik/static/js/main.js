// Main JavaScript utilities

function showSubmissions() {
    const modal = document.getElementById('submissions-modal');
    modal.style.display = 'block';
    loadSubmissions();
}

function closeSubmissions() {
    const modal = document.getElementById('submissions-modal');
    modal.style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function (event) {
    const modal = document.getElementById('submissions-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

async function loadSubmissions() {
    try {
        const response = await fetch('/api/submissions/', {
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error('Failed to load submissions');
        }

        const submissions = await response.json();
        displaySubmissions(submissions);
    } catch (error) {
        console.error('Error loading submissions:', error);
        const listContainer = document.getElementById('submissions-list');
        if (listContainer) {
            listContainer.innerHTML = '<div class="error-message">Failed to load submissions</div>';
        }
    }
}

function displaySubmissions(submissions) {
    const listContainer = document.getElementById('submissions-list');
    if (!listContainer) return;

    if (submissions.length === 0) {
        listContainer.innerHTML = '<p>No submissions yet.</p>';
        return;
    }

    listContainer.innerHTML = submissions.map(sub => `
        <div class="submission-item" onclick="viewSubmission(${sub.id})">
            <div class="submission-header">
                <span class="submission-language">${sub.language.toUpperCase()}</span>
                <span class="submission-status status-${sub.status}">${sub.status}</span>
            </div>
            <div class="submission-meta">
                <div>Time: ${new Date(sub.submitted_at).toLocaleString()}</div>
                ${sub.execution_time ? `<div>Execution: ${sub.execution_time.toFixed(3)}s</div>` : ''}
            </div>
            <div style="margin-top: 0.5rem; color: #666; font-size: 0.9rem;">
                ${sub.code_preview}
            </div>
        </div>
    `).join('');
}

async function viewSubmission(submissionId) {
    try {
        const response = await fetch(`/api/submissions/${submissionId}/`, {
            credentials: 'include'
        });

        if (!response.ok) {
            throw new Error('Failed to load submission details');
        }

        const submission = await response.json();

        // Display submission details in a new modal or alert
        alert(`Submission Details:\n\nLanguage: ${submission.language}\nStatus: ${submission.status}\n\nCode:\n${submission.code}\n\nOutput:\n${submission.output || 'N/A'}\n\nError:\n${submission.error_message || 'None'}`);
    } catch (error) {
        console.error('Error loading submission:', error);
        alert('Failed to load submission details');
    }
}

// Theme Switching Logic
function setTheme(theme) {
    const html = document.documentElement;
    localStorage.setItem('theme', theme);

    if (theme === 'system') {
        const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        html.setAttribute('data-theme', systemTheme);
    } else {
        html.setAttribute('data-theme', theme);
    }

    // Update icons
    const icon = document.querySelector('#theme-toggle i');
    if (icon) {
        if (theme === 'dark') icon.className = 'fas fa-moon';
        else if (theme === 'light') icon.className = 'fas fa-sun';
        else icon.className = 'fas fa-desktop';
    }

    const themeMenu = document.getElementById('theme-menu');
    if (themeMenu) themeMenu.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const themeMenu = document.getElementById('theme-menu');

    if (themeToggle && themeMenu) {
        themeToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            themeMenu.style.display = themeMenu.style.display === 'none' ? 'block' : 'none';
        });

        document.addEventListener('click', () => {
            themeMenu.style.display = 'none';
        });
    }

    // Set initial theme and icon
    const savedTheme = localStorage.getItem('theme') || 'system';
    setTheme(savedTheme);
});