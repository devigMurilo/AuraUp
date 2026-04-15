// Dashboard JavaScript

function inicializarGraficos(dados) {
    // Gráfico de Seguidores
    if (document.getElementById('chart-seguidores')) {
        const ctxSeguidores = document.getElementById('chart-seguidores').getContext('2d');
        const chartSeguidores = new Chart(ctxSeguidores, {
            type: 'line',
            data: {
                labels: JSON.parse(dados.seguidores.labels),
                datasets: [{
                    label: 'Seguidores',
                    data: JSON.parse(dados.seguidores.dados),
                    borderColor: '#1890ff',
                    backgroundColor: 'rgba(24, 144, 255, 0.05)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#1890ff',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            color: '#666',
                            font: { size: 12 }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#666' },
                        grid: { color: 'rgba(0, 0, 0, 0.05)' }
                    },
                    x: {
                        ticks: { color: '#666' },
                        grid: { color: 'rgba(0, 0, 0, 0.05)' }
                    }
                }
            }
        });
    }

    // Gráfico de Publicações
    if (document.getElementById('chart-publicacoes')) {
        const ctxPublicacoes = document.getElementById('chart-publicacoes').getContext('2d');
        const chartPublicacoes = new Chart(ctxPublicacoes, {
            type: 'bar',
            data: {
                labels: JSON.parse(dados.publicacoes.labels),
                datasets: [{
                    label: 'Publicações',
                    data: JSON.parse(dados.publicacoes.dados),
                    backgroundColor: '#00b96b',
                    borderColor: '#00a855',
                    borderWidth: 1,
                    borderRadius: 4,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        labels: { color: '#666', font: { size: 12 } }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#666' },
                        grid: { color: 'rgba(0, 0, 0, 0.05)' }
                    },
                    x: {
                        ticks: { color: '#666' },
                        grid: { color: 'transparent' }
                    }
                }
            }
        });
    }

    // Gráfico de Avaliações (Pie Chart)
    if (document.getElementById('chart-avaliacoes')) {
        const ctxAvaliacoes = document.getElementById('chart-avaliacoes').getContext('2d');
        const chartAvaliacoes = new Chart(ctxAvaliacoes, {
            type: 'doughnut',
            data: {
                labels: JSON.parse(dados.avaliacoes.labels),
                datasets: [{
                    data: JSON.parse(dados.avaliacoes.dados),
                    backgroundColor: JSON.parse(dados.avaliacoes.cores),
                    borderColor: '#fff',
                    borderWidth: 2,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom',
                        labels: { color: '#666', font: { size: 12 }, padding: 15 }
                    }
                }
            }
        });
    }

    // Gráfico de Top Posts
    if (document.getElementById('chart-top-posts')) {
        const ctxTopPosts = document.getElementById('chart-top-posts').getContext('2d');
        const chartTopPosts = new Chart(ctxTopPosts, {
            type: 'barH',
            data: {
                labels: JSON.parse(dados.top_posts.titulos),
                datasets: [{
                    label: 'Engajamento',
                    data: JSON.parse(dados.top_posts.engajamentos),
                    backgroundColor: '#faad14',
                    borderColor: '#f5a623',
                    borderWidth: 1,
                    borderRadius: 4,
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        labels: { color: '#666', font: { size: 12 } }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: { color: '#666' },
                        grid: { color: 'rgba(0, 0, 0, 0.05)' }
                    },
                    y: {
                        ticks: { color: '#666' },
                        grid: { color: 'transparent' }
                    }
                }
            }
        });
    }
}

// Funcionalidade de Abas
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', function() {
        const tabName = this.getAttribute('data-tab');
        
        // Remover classe active de todos os botões e abas
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        // Adicionar classe active ao botão clicado e sua aba
        this.classList.add('active');
        document.getElementById(tabName + '-tab').classList.add('active');
    });
});

// Inicializar primeira aba como ativa
document.addEventListener('DOMContentLoaded', function() {
    const primeiroTab = document.querySelector('.tab-button');
    if (primeiroTab) {
        primeiroTab.classList.add('active');
        const tabName = primeiroTab.getAttribute('data-tab');
        const tabContent = document.getElementById(tabName + '-tab');
        if (tabContent) {
            tabContent.classList.add('active');
        }
    }
});
