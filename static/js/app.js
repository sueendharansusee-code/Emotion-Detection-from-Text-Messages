// Emotion Emoji and Style Mapping
const EMOTION_META = {
    'Happy': { emoji: '😊', bg: '#ecfdf5', border: '#a7f3d0', badgeClass: 'badge-happy' },
    'Sad': { emoji: '😢', bg: '#eff6ff', border: '#bfdbfe', badgeClass: 'badge-sad' },
    'Angry': { emoji: '😡', bg: '#fef2f2', border: '#fecaca', badgeClass: 'badge-angry' },
    'Fear': { emoji: '😨', bg: '#f5f3ff', border: '#ddd6fe', badgeClass: 'badge-fear' },
    'Surprise': { emoji: '😲', bg: '#fffbebf', border: '#fde68a', badgeClass: 'badge-surprise' },
    'Neutral': { emoji: '😐', bg: '#f1f5f9', border: '#cbd5e1', badgeClass: 'badge-neutral' }
};

let sampleMessagesMap = {};
let latestAnalysisResult = null;

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    setupCounter();
    fetchSamples();
    loadDashboardStats();
    loadAnalysisHistory();
});

// Setup Live Text Counter
function setupCounter() {
    const input = document.getElementById('textInput');
    const counter = document.getElementById('liveCounter');
    const valErr = document.getElementById('validationError');

    input.addEventListener('input', () => {
        const text = input.value;
        const charCount = text.length;
        const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
        
        counter.textContent = `${charCount} chars | ${wordCount} words`;

        if (text.trim()) {
            valErr.style.display = 'none';
        }
    });
}

// Fetch Sample Messages from API
async function fetchSamples() {
    try {
        const res = await fetch('/api/samples');
        if (res.ok) {
            const data = await res.json();
            sampleMessagesMap = data.samples || {};
        }
    } catch (e) {
        console.error('Error loading sample messages:', e);
    }
}

// Insert Sample Message into Textarea
function loadSample(emotion) {
    const input = document.getElementById('textInput');
    const valErr = document.getElementById('validationError');
    
    if (sampleMessagesMap[emotion]) {
        input.value = sampleMessagesMap[emotion];
    } else {
        const fallbacks = {
            'Happy': 'I am so excited and happy about our launch today!',
            'Sad': 'I feel so lonely and heartbroken, everything went wrong.',
            'Angry': 'I am furious with this unacceptable delay and terrible service!',
            'Fear': 'Panicking because I heard strange frightening noises outside.',
            'Surprise': 'Wow, incredible! I cannot believe we won first prize!',
            'Neutral': 'The team meeting is scheduled for tomorrow at 10 AM.'
        };
        input.value = fallbacks[emotion] || '';
    }

    input.dispatchEvent(new Event('input'));
    valErr.style.display = 'none';
}

// Clear Text Input
function clearInput() {
    const input = document.getElementById('textInput');
    input.value = '';
    input.dispatchEvent(new Event('input'));
}

// Main Analyze Function
async function analyzeText() {
    const input = document.getElementById('textInput');
    const text = input.value.trim();
    const valErr = document.getElementById('validationError');
    const errMsg = document.getElementById('errorMessage');
    const btn = document.getElementById('analyzeBtn');
    const btnIcon = document.getElementById('btnIcon');
    const btnText = document.getElementById('btnText');

    if (!text) {
        errMsg.textContent = "Validation Error: Please enter a text message to analyze.";
        valErr.style.display = 'flex';
        input.focus();
        return;
    }

    valErr.style.display = 'none';

    // Show Loading State
    btn.disabled = true;
    btnIcon.className = "fa-solid fa-spinner fa-spin";
    btnText.textContent = "Analyzing...";

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to analyze text message.');
        }

        latestAnalysisResult = data;
        displayResult(data);

        // Refresh stats & history
        await loadDashboardStats();
        await loadAnalysisHistory();

        showToast("Emotion analysis complete!");

    } catch (err) {
        errMsg.textContent = err.message;
        valErr.style.display = 'flex';
    } finally {
        btn.disabled = false;
        btnIcon.className = "fa-solid fa-magnifying-glass-chart";
        btnText.textContent = "Analyze Emotion";
    }
}

// Display Analysis Output
function displayResult(data) {
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('resultContent').style.display = 'flex';
    document.getElementById('copyBtn').style.display = 'flex';

    const emo = data.predicted_emotion;
    const meta = EMOTION_META[emo] || EMOTION_META['Neutral'];

    // Update Prediction Banner
    const banner = document.getElementById('predictionBanner');
    banner.style.backgroundColor = meta.bg;
    banner.style.borderColor = meta.border;

    document.getElementById('emotionEmoji').textContent = meta.emoji;
    document.getElementById('predictedEmotion').textContent = emo;
    document.getElementById('confidenceValue').textContent = `${data.confidence_score}%`;
    document.getElementById('disclaimerText').textContent = data.disclaimer;

    // Text Stats
    const stats = data.text_statistics || {};
    document.getElementById('statCharCount').textContent = stats.char_count || 0;
    document.getElementById('statWordCount').textContent = stats.word_count || 0;
    document.getElementById('statAvgWordLen').textContent = stats.avg_word_len || 0;
    document.getElementById('statUniqueWords').textContent = stats.unique_word_count || 0;

    // Probability Chart
    renderProbabilityChart(data.probabilities);
}

// Copy Analysis Result to Clipboard
function copyResult() {
    if (!latestAnalysisResult) return;

    const summary = 
`[Emotion Detection Result]
Text: "${latestAnalysisResult.text}"
Expressed Emotion: ${latestAnalysisResult.predicted_emotion}
Confidence Score: ${latestAnalysisResult.confidence_score}%
Text Stats: ${latestAnalysisResult.text_statistics.word_count} words | ${latestAnalysisResult.text_statistics.char_count} chars
Notice: ${latestAnalysisResult.disclaimer}`;

    navigator.clipboard.writeText(summary).then(() => {
        showToast("Result copied to clipboard!");
    }).catch(() => {
        showToast("Failed to copy result.");
    });
}

// Fetch and Render Dashboard Stats
async function loadDashboardStats() {
    try {
        const res = await fetch('/api/stats');
        if (res.ok) {
            const data = await res.json();
            document.getElementById('statTotalAnalyzed').textContent = data.total_analyzed || 0;
            document.getElementById('statTopEmotion').textContent = data.top_emotion || 'None';
            document.getElementById('statAvgConfidence').textContent = `${data.avg_confidence || 0}%`;

            renderHistoryDistributionChart(data.emotion_counts || {});
        }
    } catch (e) {
        console.error('Error loading dashboard stats:', e);
    }
}

// Fetch and Render Analysis History
async function loadAnalysisHistory() {
    const filter = document.getElementById('emotionFilter').value;
    try {
        const res = await fetch(`/api/history?emotion=${encodeURIComponent(filter)}`);
        if (res.ok) {
            const data = await res.json();
            renderHistoryTable(data.history || []);
        }
    } catch (e) {
        console.error('Error loading history:', e);
    }
}

function filterHistory() {
    loadAnalysisHistory();
}

function renderHistoryTable(logs) {
    const tbody = document.getElementById('historyTableBody');
    tbody.innerHTML = '';

    if (logs.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center">No analysis history available.</td></tr>`;
        return;
    }

    logs.forEach(log => {
        const tr = document.createElement('tr');
        const meta = EMOTION_META[log.predicted_emotion] || EMOTION_META['Neutral'];
        
        // Format timestamp
        const timeStr = log.created_at ? new Date(log.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '-';

        tr.innerHTML = `
            <td>${timeStr}</td>
            <td class="text-snippet" title="${escapeHtml(log.text)}">${escapeHtml(log.text)}</td>
            <td><span class="badge ${meta.badgeClass}">${meta.emoji} ${log.predicted_emotion}</span></td>
            <td><strong>${log.confidence_score}%</strong></td>
            <td>${log.word_count || 0}</td>
        `;
        tbody.appendChild(tr);
    });
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Clear History Modal Handlers
function confirmClearHistory() {
    document.getElementById('clearModal').style.display = 'flex';
}

function closeClearModal() {
    document.getElementById('clearModal').style.display = 'none';
}

async function executeClearHistory() {
    try {
        const res = await fetch('/api/clear-history', { method: 'POST' });
        if (res.ok) {
            closeClearModal();
            showToast("History cleared successfully.");
            await loadDashboardStats();
            await loadAnalysisHistory();
        }
    } catch (e) {
        console.error('Error clearing history:', e);
    }
}

// Show Toast Notification
function showToast(message) {
    const toast = document.getElementById('toastNotification');
    const msg = document.getElementById('toastMessage');
    msg.textContent = message;
    
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
