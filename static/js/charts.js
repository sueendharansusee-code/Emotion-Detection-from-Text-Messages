// Chart Instances
let probabilityChartInstance = null;
let historyChartInstance = null;

const EMOTION_COLORS = {
    'Happy': '#10b981',
    'Sad': '#3b82f6',
    'Angry': '#ef4444',
    'Fear': '#8b5cf6',
    'Surprise': '#f59e0b',
    'Neutral': '#64748b'
};

const EMOTION_BG_COLORS = {
    'Happy': 'rgba(16, 185, 129, 0.2)',
    'Sad': 'rgba(59, 130, 246, 0.2)',
    'Angry': 'rgba(239, 68, 68, 0.2)',
    'Fear': 'rgba(139, 92, 246, 0.2)',
    'Surprise': 'rgba(245, 158, 11, 0.2)',
    'Neutral': 'rgba(100, 116, 139, 0.2)'
};

/**
 * Render Probability Horizontal Bar Chart for current prediction
 */
function renderProbabilityChart(probabilities) {
    const ctx = document.getElementById('probabilityChart').getContext('2d');

    const labels = ['Happy', 'Sad', 'Angry', 'Fear', 'Surprise', 'Neutral'];
    const data = labels.map(label => probabilities[label] || 0);
    const borderColors = labels.map(label => EMOTION_COLORS[label]);
    const backgroundColors = labels.map(label => EMOTION_BG_COLORS[label]);

    if (probabilityChartInstance) {
        probabilityChartInstance.destroy();
    }

    probabilityChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Confidence (%)',
                data: data,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 1.5,
                borderRadius: 6
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 2.2,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return ` ${context.raw}% probability`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: '#e2e8f0' },
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                },
                y: {
                    grid: { display: false }
                }
            }
        }
    });
}

/**
 * Render Historical Emotion Distribution Doughnut Chart
 */
function renderHistoryDistributionChart(emotionCounts) {
    const ctx = document.getElementById('historyDistributionChart').getContext('2d');

    const labels = ['Happy', 'Sad', 'Angry', 'Fear', 'Surprise', 'Neutral'];
    const data = labels.map(label => emotionCounts[label] || 0);
    const backgroundColors = labels.map(label => EMOTION_COLORS[label]);

    if (historyChartInstance) {
        historyChartInstance.destroy();
    }

    historyChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
                borderWidth: 2,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        padding: 14,
                        font: { family: 'Inter', size: 12 }
                    }
                }
            },
            cutout: '65%'
        }
    });
}
