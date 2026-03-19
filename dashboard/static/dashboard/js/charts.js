/* ============================================================
   Netflix Dashboard — charts.js
   All Chart.js configurations + search + filters
   ============================================================ */

const NETFLIX_RED   = '#E50914';
const NETFLIX_RED2  = '#B20710';
const NETFLIX_RED3  = '#6B0F1A';
const NETFLIX_RED4  = '#3D0A0F';
const BLUE_MUTED    = '#8AB4F8';
const SURFACE       = '#1C1C1C';
const BORDER_COLOR  = 'rgba(255,255,255,0.06)';
const TEXT_MUTED    = '#A0A0A0';
const TEXT_DIM      = '#606060';

// ──────────────────────────────────────────────
//  Chart.js global defaults
// ──────────────────────────────────────────────
Chart.defaults.color = TEXT_MUTED;
Chart.defaults.borderColor = BORDER_COLOR;
Chart.defaults.font.family = "'Inter', system-ui, sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.plugins.legend.display = false;
Chart.defaults.plugins.tooltip.backgroundColor = '#1C1C1C';
Chart.defaults.plugins.tooltip.borderColor = 'rgba(255,255,255,0.12)';
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.titleColor = '#fff';
Chart.defaults.plugins.tooltip.bodyColor = TEXT_MUTED;
Chart.defaults.plugins.tooltip.padding = 10;
Chart.defaults.plugins.tooltip.cornerRadius = 6;

// ──────────────────────────────────────────────
//  Pie Chart — Movie vs TV Show
// ──────────────────────────────────────────────
function initPieChart(labels, values) {
  const ctx = document.getElementById('pieChart');
  if (!ctx) return;

  const colors = [NETFLIX_RED, '#564D4D', NETFLIX_RED3, '#333'];
  new Chart(ctx, {
    type: 'pie',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors.slice(0, values.length),
        borderColor: '#141414',
        borderWidth: 3,
        hoverOffset: 6,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.label}: ${ctx.parsed.toLocaleString('fr-FR')} (${(ctx.parsed / ctx.dataset.data.reduce((a,b)=>a+b,0)*100).toFixed(1)}%)`,
          }
        }
      }
    }
  });

  // Custom legend
  const total = values.reduce((a, b) => a + b, 0);
  const legend = document.getElementById('pieLegend');
  if (legend) {
    legend.innerHTML = labels.map((l, i) =>
      `<span class="legend-item">
        <span class="legend-swatch" style="background:${colors[i]}"></span>
        ${l} <span style="color:#fff;font-weight:600">${(values[i] / total * 100).toFixed(1)}%</span>
       </span>`
    ).join('');
  }
}

// ──────────────────────────────────────────────
//  Bar Chart — Top 10 Genres
// ──────────────────────────────────────────────
function initBarChart(labels, values) {
  const ctx = document.getElementById('barChart');
  if (!ctx) return;

  // Gradient colors from bright red to dark
  const palette = [
    NETFLIX_RED, '#D4080D', '#BF060B', '#AA0509',
    '#950407', '#800306', '#6B0204', '#560102',
    '#410101', '#2C0000'
  ];

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: labels.map((_, i) => palette[i] || NETFLIX_RED4),
        borderRadius: 3,
        borderSkipped: false,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: {
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.parsed.x.toLocaleString('fr-FR')} titres`
          }
        }
      },
      scales: {
        x: {
          grid: { color: BORDER_COLOR },
          ticks: { color: TEXT_DIM },
        },
        y: {
          grid: { display: false },
          ticks: {
            color: '#ccc',
            font: { size: 11 },
          }
        }
      }
    }
  });
}

// ──────────────────────────────────────────────
//  Line Chart — Evolution by release_year
// ──────────────────────────────────────────────
function initLineChart(labels, values) {
  const ctx = document.getElementById('lineChart');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        data: values,
        borderColor: NETFLIX_RED,
        backgroundColor: 'rgba(229,9,20,0.12)',
        fill: true,
        tension: 0.4,
        pointBackgroundColor: NETFLIX_RED,
        pointBorderColor: '#141414',
        pointBorderWidth: 2,
        pointRadius: 3,
        pointHoverRadius: 6,
        borderWidth: 2.5,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.parsed.y.toLocaleString('fr-FR')} titres`
          }
        }
      },
      scales: {
        x: {
          grid: { color: BORDER_COLOR },
          ticks: { color: TEXT_DIM, maxRotation: 45 }
        },
        y: {
          grid: { color: BORDER_COLOR },
          ticks: {
            color: TEXT_DIM,
            callback: v => v >= 1000 ? (v/1000).toFixed(1) + 'k' : v
          }
        }
      }
    }
  });
}

// ──────────────────────────────────────────────
//  Donut Chart — Rating Category
// ──────────────────────────────────────────────
function initDonutChart(labels, values) {
  const ctx = document.getElementById('donutChart');
  if (!ctx) return;

  const colorMap = {
    'Adult':   NETFLIX_RED,
    'Teen':    '#B8141F',
    'Kids':    '#6B0F1A',
    'Unknown': '#444444',
  };
  const colors = labels.map(l => colorMap[l] || '#555');
  const total = values.reduce((a, b) => a + b, 0);

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors,
        borderColor: '#141414',
        borderWidth: 3,
        hoverOffset: 5,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '68%',
      plugins: {
        tooltip: {
          callbacks: {
            label: ctx => ` ${ctx.label}: ${(ctx.parsed / total * 100).toFixed(1)}%`
          }
        }
      }
    }
  });

  // Legend
  const legend = document.getElementById('donutLegend');
  if (legend) {
    legend.innerHTML = labels.map((l, i) =>
      `<span class="legend-item">
        <span class="legend-swatch" style="background:${colors[i]}"></span>
        ${l} <span style="color:#fff;font-weight:600">${(values[i] / total * 100).toFixed(1)}%</span>
       </span>`
    ).join('');
  }
}

// ──────────────────────────────────────────────
//  Duration histogram (analysis page)
// ──────────────────────────────────────────────
function initDurationChart(labels, values) {
  const ctx = document.getElementById('durationChart');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: NETFLIX_RED,
        borderRadius: 3,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.y} films` } } },
      scales: {
        x: { grid: { color: BORDER_COLOR }, ticks: { color: TEXT_DIM } },
        y: { grid: { color: BORDER_COLOR }, ticks: { color: TEXT_DIM } }
      }
    }
  });
}

// ──────────────────────────────────────────────
//  Seasons distribution
// ──────────────────────────────────────────────
function initSeasonsChart(labels, values) {
  const ctx = document.getElementById('seasonsChart');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: NETFLIX_RED2,
        borderRadius: 3,
        indexAxis: 'y',
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: { tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.x} séries` } } },
      scales: {
        x: { grid: { color: BORDER_COLOR }, ticks: { color: TEXT_DIM } },
        y: { grid: { display: false }, ticks: { color: '#ccc' } }
      }
    }
  });
}

// ──────────────────────────────────────────────
//  Raw ratings bar
// ──────────────────────────────────────────────
function initRatingRawChart(labels, values) {
  const ctx = document.getElementById('ratingRawChart');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: labels.map((_, i) =>
          `rgba(229,9,20,${Math.max(0.2, 1 - i * 0.08)})`
        ),
        borderRadius: 4,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { tooltip: { callbacks: { label: ctx => ` ${ctx.parsed.y.toLocaleString()} titres` } } },
      scales: {
        x: { grid: { display: false }, ticks: { color: '#ccc' } },
        y: { grid: { color: BORDER_COLOR }, ticks: { color: TEXT_DIM } }
      }
    }
  });
}

// ──────────────────────────────────────────────
//  Added per year (stacked area)
// ──────────────────────────────────────────────
function initAddedChart(labels, values) {
  const ctx = document.getElementById('addedChart');
  if (!ctx) return;
  new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        data: values,
        borderColor: NETFLIX_RED,
        backgroundColor: 'rgba(229,9,20,0.15)',
        fill: true,
        tension: 0.4,
        pointRadius: 3,
        pointBackgroundColor: NETFLIX_RED,
        borderWidth: 2,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { grid: { color: BORDER_COLOR }, ticks: { color: TEXT_DIM } },
        y: { grid: { color: BORDER_COLOR }, ticks: { color: TEXT_DIM } }
      }
    }
  });
}

// ──────────────────────────────────────────────
//  Live search
// ──────────────────────────────────────────────
(function initSearch() {
  const input = document.getElementById('searchInput');
  const results = document.getElementById('searchResults');
  if (!input || !results) return;

  let timer;
  input.addEventListener('input', () => {
    clearTimeout(timer);
    const q = input.value.trim();
    if (q.length < 2) { results.classList.remove('open'); return; }
    timer = setTimeout(() => fetchSearch(q), 250);
  });

  document.addEventListener('click', e => {
    if (!e.target.closest('.search-wrap')) results.classList.remove('open');
  });

  async function fetchSearch(q) {
    try {
      const res = await fetch(`/api/search/?q=${encodeURIComponent(q)}`);
      const data = await res.json();
      if (!data.results.length) {
        results.innerHTML = '<div class="search-result-item"><span class="muted">Aucun résultat</span></div>';
      } else {
        results.innerHTML = data.results.map(r =>
          `<div class="search-result-item">
            <div class="sri-title">
              <span class="badge ${r.type === 'Movie' ? 'badge-movie' : 'badge-tv'}">${r.type}</span>
              ${r.title}
            </div>
            <div class="sri-meta">
              ${r.release_year || '—'} · ${r.country || '—'} · ${r.primary_genre || '—'}
            </div>
           </div>`
        ).join('');
      }
      results.classList.add('open');
    } catch (e) {
      console.error('Search error:', e);
    }
  }
})();

// ──────────────────────────────────────────────
//  Animate KPI counters on load
// ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.kpi-value[data-target]').forEach(el => {
    const target = parseInt(el.dataset.target, 10);
    const duration = 1200;
    const step = target / (duration / 16);
    let current = 0;
    const timer = setInterval(() => {
      current = Math.min(current + step, target);
      el.textContent = Math.round(current).toLocaleString('fr-FR');
      if (current >= target) clearInterval(timer);
    }, 16);
  });
});
