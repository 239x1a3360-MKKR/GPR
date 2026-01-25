// Code Editor JavaScript

let editor;
let currentLanguage = 'python';

// Initialize CodeMirror editor
document.addEventListener('DOMContentLoaded', function () {
    const savedCode = localStorage.getItem(`practice_code_${currentLanguage}`);

    editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
        lineNumbers: true,
        theme: 'monokai',
        mode: 'python',
        indentUnit: 4,
        indentWithTabs: false,
        lineWrapping: true,
        autoCloseBrackets: true,
        matchBrackets: true,
    });

    if (savedCode) {
        editor.setValue(savedCode);
    } else {
        setDefaultCode('python');
    }

    // Auto-save logic
    setInterval(() => {
        const currentCode = editor.getValue();
        if (currentCode.trim()) {
            localStorage.setItem(`practice_code_${currentLanguage}`, currentCode);
        }
    }, 2000);
});

function changeLanguage() {
    const language = document.getElementById('language').value;
    currentLanguage = language;

    let mode;
    switch (language) {
        case 'python':
            mode = 'python';
            break;
        case 'c':
        case 'cpp':
            mode = 'text/x-c++src';
            break;
        case 'java':
            mode = 'text/x-java';
            break;
        default:
            mode = 'text/plain';
    }

    editor.setOption('mode', mode);

    const savedCode = localStorage.getItem(`practice_code_${language}`);
    if (savedCode) {
        editor.setValue(savedCode);
    } else {
        setDefaultCode(language);
    }
}

function setDefaultCode(language) {
    const defaultCodes = {
        python: `# Python Program
print("Hello, World!")

# Add your code here
`,
        c: `#include <stdio.h>

int main() {
    printf("Hello, World!\\n");
    
    // Add your code here
    
    return 0;
}
`,
        cpp: `#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    
    // Add your code here
    
    return 0;
}
`,
        java: `public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
        
        // Add your code here
    }
}
`
    };

    editor.setValue(defaultCodes[language] || '');
}

function resetCode() {
    if (confirm('Are you sure you want to reset the editor? This will clear your current code.')) {
        setDefaultCode(currentLanguage);
    }
}

async function runCode() {
    const code = editor.getValue();
    const inputData = document.getElementById('input-data').value;
    const outputDisplay = document.getElementById('output-display');
    const loading = document.getElementById('loading');

    if (!code.trim()) {
        alert('Please enter some code to execute');
        return;
    }

    // Show loading
    loading.style.display = 'flex';
    outputDisplay.innerHTML = '<div class="output-placeholder">Executing...</div>';
    outputDisplay.className = 'output-display';

    try {
        const response = await fetch('/api/execute/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify({
                language: currentLanguage,
                code: code,
                input: inputData
            })
        });

        if (!response.ok) {
            let errorData;
            try {
                errorData = await response.json();
            } catch (e) {
                errorData = { error: 'Execution failed' };
            }
            throw new Error(errorData.error || 'Execution failed');
        }

        const result = await response.json();

        // Hide loading
        loading.style.display = 'none';

        // Display results
        let outputHTML = '';

        if (result.execution_time) {
            outputHTML += `<div class="execution-info">Execution Time: ${result.execution_time}s</div>`;
        }

        if (result.success) {
            outputDisplay.className = 'output-display output-success';
            outputHTML += result.output || '(No output)';
        } else {
            outputDisplay.className = 'output-display output-error';
            outputHTML += result.error || 'Execution failed';
            if (result.output) {
                outputHTML += '\n\nOutput:\n' + result.output;
            }
        }

        outputDisplay.innerHTML = outputHTML;

    } catch (error) {
        loading.style.display = 'none';
        outputDisplay.className = 'output-display output-error';
        outputDisplay.innerHTML = `Error: ${error.message}`;
    }
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

