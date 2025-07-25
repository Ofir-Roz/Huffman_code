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
    
    // Display Huffman tree visualization
    if (data.tree_structure && Object.keys(data.tree_structure).length > 0) {
        renderHuffmanTree(data.tree_structure);
        document.getElementById('treeSection').style.display = 'block';
    }
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
    document.getElementById('treeSection').style.display = 'none';
    
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

/**
 * Render the Huffman tree visualization using SVG
 * @param {Object} treeData - Tree structure data from the backend
 */
function renderHuffmanTree(treeData) {
    const svg = document.getElementById('treeCanvas');
    const container = svg.parentElement;
    
    // Clear previous tree
    svg.innerHTML = '';
    
    if (!treeData || Object.keys(treeData).length === 0) {
        return;
    }
    
    // Calculate tree dimensions for more cubic layout
    const maxDepth = calculateTreeDepth(treeData);
    const leafCount = countLeafNodes(treeData);
    
    // More balanced dimensions - less wide, more proportional
    const treeWidth = Math.min(1000, Math.max(600, leafCount * 60));
    const treeHeight = Math.max(400, maxDepth * 80);
    
    // Set SVG dimensions
    svg.setAttribute('width', treeWidth);
    svg.setAttribute('height', treeHeight);
    svg.setAttribute('viewBox', `0 0 ${treeWidth} ${treeHeight}`);
    
    // Render the tree recursively
    renderTreeNode(svg, treeData);
}

/**
 * Calculate the maximum depth of the tree
 * @param {Object} node - Tree node
 * @returns {number} Maximum depth
 */
function calculateTreeDepth(node) {
    if (!node || !node.children || node.children.length === 0) {
        return 1;
    }
    
    let maxChildDepth = 0;
    node.children.forEach(child => {
        maxChildDepth = Math.max(maxChildDepth, calculateTreeDepth(child));
    });
    
    return 1 + maxChildDepth;
}

/**
 * Count the number of leaf nodes in the tree
 * @param {Object} node - Tree node
 * @returns {number} Number of leaf nodes
 */
function countLeafNodes(node) {
    if (!node) {
        return 0;
    }
    
    if (!node.children || node.children.length === 0) {
        return 1;
    }
    
    let leafCount = 0;
    node.children.forEach(child => {
        leafCount += countLeafNodes(child);
    });
    
    return leafCount;
}

/**
 * Render a single tree node and its children
 * @param {SVGElement} svg - SVG container
 * @param {Object} node - Node data
 */
function renderTreeNode(svg, node) {
    const nodeRadius = 25;
    const x = node.x;
    const y = node.y;
    
    // Draw connections to children first (so they appear behind nodes)
    if (node.children && node.children.length > 0) {
        node.children.forEach((child, index) => {
            const childX = child.x;
            const childY = child.y;
            
            // Draw line
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', x);
            line.setAttribute('y1', y);
            line.setAttribute('x2', childX);
            line.setAttribute('y2', childY);
            line.setAttribute('class', 'tree-link');
            svg.appendChild(line);
            
            // Draw edge label (0 for left, 1 for right)
            const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            label.setAttribute('x', (x + childX) / 2);
            label.setAttribute('y', (y + childY) / 2 - 5);
            label.setAttribute('class', 'tree-edge-label');
            label.textContent = child.side === 'left' ? '0' : '1';
            svg.appendChild(label);
            
            // Recursively draw child
            renderTreeNode(svg, child);
        });
    }
    
    // Draw node circle
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', x);
    circle.setAttribute('cy', y);
    circle.setAttribute('r', nodeRadius);
    circle.setAttribute('class', `tree-node ${node.is_leaf ? 'leaf' : ''}`);
    
    // Add hover title
    const title = document.createElementNS('http://www.w3.org/2000/svg', 'title');
    if (node.is_leaf) {
        title.textContent = `Character: "${node.char}" | Frequency: ${node.frequency} | Code: ${node.code}`;
    } else {
        title.textContent = `Internal Node | Frequency: ${node.frequency}`;
    }
    circle.appendChild(title);
    
    svg.appendChild(circle);
    
    // Draw node text
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', x);
    text.setAttribute('y', y + 4);
    text.setAttribute('class', 'tree-text');
    
    if (node.is_leaf) {
        // Display character for leaf nodes
        const displayChar = node.char === ' ' ? '␣' : 
                          node.char === '\n' ? '\\n' : 
                          node.char === '\t' ? '\\t' : 
                          node.char;
        text.textContent = displayChar;
    } else {
        // Display frequency for internal nodes
        text.textContent = node.frequency;
    }
    
    svg.appendChild(text);
    
    // Add frequency text below node for leaf nodes
    if (node.is_leaf) {
        const freqText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        freqText.setAttribute('x', x);
        freqText.setAttribute('y', y + nodeRadius + 15);
        freqText.setAttribute('class', 'tree-text frequency');
        freqText.textContent = `f:${node.frequency}`;
        svg.appendChild(freqText);
    }
}
