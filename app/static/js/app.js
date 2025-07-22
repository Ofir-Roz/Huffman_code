/* Huffman Coding Compressor JavaScript */

// Global state to store current encoding data
let currentData = {
    encoded: '',
    frequency_table: [],
    huffmanCodes: [],
    operation: 'encode' // Track current operation
};

/**
 * Show success or error messages to the user
 * @param {string} message - Message to display
 * @param {string} type - 'error' or 'success'
 */
function showMessage(message, type) {
    const errorEl = document.getElementById('errorMessage');
    const successEl = document.getElementById('successMessage');
    
    errorEl.style.display = 'none';
    successEl.style.display = 'none';
    
    if (type === 'error') {
        errorEl.textContent = message;
        errorEl.style.display = 'block';
    } else {
        successEl.textContent = message;
        successEl.style.display = 'block';
    }
    
    // Auto-hide messages after 5 seconds
    setTimeout(() => {
        errorEl.style.display = 'none';
        successEl.style.display = 'none';
    }, 5000);
}

/**
 * Show or hide loading indicator
 * @param {boolean} show - Whether to show loading indicator
 */
function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

/**
 * Encode text using Huffman coding algorithm
 */
async function encodeText() {
    const text = document.getElementById('inputText').value;
    
    if (!text.trim()) {
        showMessage('Please enter some text to encode!', 'error');
        return;
    }

    showLoading(true);
    
    try {
        const response = await fetch('/encode', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Encoding failed');
        }

        currentData = data;
        currentData.operation = 'encode';
        displayEncodeResults(data);
        showMessage('Text encoded successfully!', 'success');
        
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

/**
 * Decode previously encoded text
 */
async function decodeText() {
    if (!currentData.encoded || !currentData.frequency_table) {
        showMessage('No encoded data available. Please encode some text first!', 'error');
        return;
    }

    showLoading(true);
    
    try {
        const response = await fetch('/decode', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                encoded: currentData.encoded,
                frequency_table: currentData.frequency_table
            })
        });

        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Decoding failed');
        }

        currentData.operation = 'decode';
        displayDecodeResults(data);
        showMessage('Text decoded successfully!', 'success');
        
    } catch (error) {
        showMessage('Error: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

/**
 * Display encoding results in the UI
 * @param {Object} data - Response data from encoding API
 */
function displayEncodeResults(data) {
    // Update title and display encoded binary
    document.getElementById('outputTitle').textContent = '💻 Encoded Output';
    document.getElementById('outputContent').textContent = data.encoded;

    // Show copy button
    document.getElementById('copyToInputBtn').style.display = 'block';

    // Display statistics
    const stats = data.stats;
    document.getElementById('originalSize').textContent = stats.original_size;
    document.getElementById('compressedSize').textContent = stats.compressed_size;
    document.getElementById('compressionRatio').textContent = (stats.compression_ratio * 100).toFixed(1) + '%';
    document.getElementById('spaceSaved').textContent = stats.space_saved.toFixed(1) + '%';
    document.getElementById('statsSection').style.display = 'block';

    // Display frequency table
    const freqTableBody = document.getElementById('frequencyTableBody');
    freqTableBody.innerHTML = '';
    data.frequency_table.forEach(item => {
        const row = document.createElement('div');
        row.className = 'table-row';
        const displayChar = item.char === ' ' ? '␣' : item.char === '\n' ? '\\n' : item.char === '\t' ? '\\t' : item.char;
        row.innerHTML = `<div>${displayChar}</div><div>${item.freq}</div>`;
        freqTableBody.appendChild(row);
    });
    document.getElementById('frequencyTable').style.display = 'block';

    // Display Huffman codes
    const codesTableBody = document.getElementById('codesTableBody');
    codesTableBody.innerHTML = '';
    data.huffman_codes.forEach(item => {
        const row = document.createElement('div');
        row.className = 'table-row';
        const displayChar = item.char === ' ' ? '␣' : item.char === '\n' ? '\\n' : item.char === '\t' ? '\\t' : item.char;
        row.innerHTML = `<div>${displayChar}</div><div>${item.code}</div>`;
        codesTableBody.appendChild(row);
    });
    document.getElementById('codesTable').style.display = 'block';
}

/**
 * Display decoding results in the UI
 * @param {Object} data - Response data from decoding API
 */
function displayDecodeResults(data) {
    // Update title and display decoded text
    document.getElementById('outputTitle').textContent = '🔓 Decoded Output';
    document.getElementById('outputContent').textContent = data.decoded;

    // Show copy button
    document.getElementById('copyToInputBtn').style.display = 'block';

    // Hide statistics and tables for decode operation
    document.getElementById('statsSection').style.display = 'none';
    document.getElementById('frequencyTable').style.display = 'none';
    document.getElementById('codesTable').style.display = 'none';
}

/**
 * Clear all data and reset the interface
 */
function clearAll() {
    document.getElementById('inputText').value = '';
    document.getElementById('outputTitle').textContent = '💻 Output';
    document.getElementById('outputContent').textContent = 'Results will appear here...';
    document.getElementById('copyToInputBtn').style.display = 'none';
    document.getElementById('frequencyTable').style.display = 'none';
    document.getElementById('codesTable').style.display = 'none';
    document.getElementById('statsSection').style.display = 'none';
    
    currentData = {
        encoded: '',
        frequency_table: [],
        huffmanCodes: [],
        operation: 'encode'
    };
    
    showMessage('All data cleared!', 'success');
}

/**
 * Copy current output text to input field for easy testing
 */
function copyToInput() {
    const outputContent = document.getElementById('outputContent').textContent;
    
    if (outputContent && outputContent !== 'Results will appear here...') {
        document.getElementById('inputText').value = outputContent;
        
        if (currentData.operation === 'encode') {
            showMessage('Encoded text copied to input!', 'success');
        } else {
            showMessage('Decoded text copied to input!', 'success');
        }
    } else {
        showMessage('No output to copy!', 'error');
    }
}
