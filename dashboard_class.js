class Dashboard {
    constructor() {
        this.initCharts();
        this.loadData('1mo');
        this.initEventListeners();
    }

    initEventListeners() {
        document.querySelectorAll('.period-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.loadData(btn.dataset.period);
            });
        });
    }

    async loadData(period) {
        try {
            const [stocks, crypto] = await Promise.all([
                this.fetchData('/api/stocks?period=' + period),
                this.fetchData('/api/crypto?period=' + period)
            ]);
            
            this.updateCharts(stocks, crypto);
        } catch (error) {
            this.showError('Failed to load data');
        }
    }

    async fetchData(url) {
        const response = await fetch(url, {
            headers: {
                'Authorization': 'Bearer ' + localStorage.getItem('token')
            }
        });
        if (!response.ok) throw new Error('API error');
        return response.json();
    }

    initCharts() {
        this.stockChart = new Chart(document.getElementById('stockChart'), {
            type: 'line',
            options: { responsive: true, maintainAspectRatio: false }
        });
        
        this.cryptoChart = new Chart(document.getElementById('cryptoChart'), {
            type: 'line',
            options: { responsive: true, maintainAspectRatio: false }
        });
    }

    updateCharts(stocks, crypto) {
        this.updateChart(this.stockChart, stocks);
        this.updateChart(this.cryptoChart, crypto);
    }

    updateChart(chart, data) {
        chart.data = {
            labels: Object.values(data)[0].history.map(d => d.date),
            datasets: [{
                label: 'Price History',
                data: Object.values(data)[0].history.map(d => d.price),
                borderColor: '#2962ff',
                tension: 0.4
            }]
        };
        chart.update();
    }

    showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        errorDiv.textContent = message;
        errorDiv.classList.remove('d-none');
    }
}

// Initialize dashboard when DOM loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('stockChart')) {
        new Dashboard();
    }
});