/**
 * script.js - Vanilla JavaScript for dynamic subject management and client interactions.
 * 
 * Features:
 * - Dynamically add new subject input rows (name="subject[]", name="teacher[]", name="classes[]")
 * - Remove subject rows
 * - Fast sample data loader for quick testing and viva demonstration
 * - Client-side validation to catch empty or negative inputs before submission
 */

// Function to add a new subject row to the form
function addSubject(subjectVal = '', teacherVal = '', classesVal = '') {
    const container = document.getElementById('subject-container');

    // Create the outer wrapper div
    const row = document.createElement('div');
    row.className = 'subject-row';

    // Populate row HTML with proper input names
    row.innerHTML = `
        <div class="form-group">
            <label class="mobile-label">Subject Name</label>
            <input 
                type="text" 
                name="subject[]" 
                placeholder="e.g. Operating System" 
                value="${escapeHtml(subjectVal)}"
                required
            >
        </div>
        <div class="form-group">
            <label class="mobile-label">Teacher Name</label>
            <input 
                type="text" 
                name="teacher[]" 
                placeholder="e.g. Prof. Verma" 
                value="${escapeHtml(teacherVal)}"
                required
            >
        </div>
        <div class="form-group">
            <label class="mobile-label">Classes/Week</label>
            <input 
                type="number" 
                name="classes[]" 
                min="1" 
                max="30" 
                placeholder="e.g. 3" 
                value="${classesVal}"
                required
            >
        </div>
        <div class="action-cell">
            <button type="button" class="btn-remove" onclick="removeSubject(this)" title="Remove this subject">✕</button>
        </div>
    `;

    // Append to container
    container.appendChild(row);

    // Smooth scroll to new row if added dynamically by user
    if (!subjectVal) {
        row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// Function to remove a subject row
function removeSubject(buttonElement) {
    const container = document.getElementById('subject-container');
    const rows = container.getElementsByClassName('subject-row');

    // Ensure at least one subject row remains
    if (rows.length > 1) {
        const row = buttonElement.closest('.subject-row');
        row.remove();
    } else {
        alert("You must keep at least one subject row.");
    }
}

// Helper to escape HTML characters in pre-filled strings
function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Helper to load standard test data (as described in Section 17 of project specification)
function loadSampleData() {
    const sampleSubjects = [
        { subject: "Artificial Intelligence", teacher: "Dr. Sharma", classes: 4 },
        { subject: "Machine Learning", teacher: "Prof. Kumar", classes: 4 },
        { subject: "Database Management System", teacher: "Dr. Singh", classes: 3 },
        { subject: "Operating System", teacher: "Prof. Verma", classes: 3 },
        { subject: "Computer Networks", teacher: "Dr. Gupta", classes: 3 }
    ];

    const container = document.getElementById('subject-container');
    // Clear existing rows
    container.innerHTML = '';

    // Add each sample subject row
    sampleSubjects.forEach(item => {
        addSubject(item.subject, item.teacher, item.classes);
    });
}

// Client-side form validation before submitting
function validateForm() {
    const subjects = document.getElementsByName('subject[]');
    const teachers = document.getElementsByName('teacher[]');
    const classes = document.getElementsByName('classes[]');

    if (subjects.length === 0) {
        alert("Please add at least one subject before generating.");
        return false;
    }

    let totalClasses = 0;

    for (let i = 0; i < subjects.length; i++) {
        const sub = subjects[i].value.trim();
        const teacher = teachers[i].value.trim();
        const count = parseInt(classes[i].value, 10);

        if (!sub) {
            alert(`Row ${i + 1}: Subject name cannot be empty.`);
            subjects[i].focus();
            return false;
        }

        if (!teacher) {
            alert(`Row ${i + 1}: Teacher name cannot be empty.`);
            teachers[i].focus();
            return false;
        }

        if (isNaN(count) || count <= 0) {
            alert(`Row ${i + 1}: Please enter a valid positive number of classes.`);
            classes[i].focus();
            return false;
        }

        totalClasses += count;
    }

    if (totalClasses > 30) {
        alert(`Total classes requested (${totalClasses}) exceeds available weekly slots (30). Please decrease the number of classes.`);
        return false;
    }

    return true;
}
