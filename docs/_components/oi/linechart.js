function initLineChart() {
  const lineChartReady = new CustomEvent("oi-linechart-ready");
  if (document.head.querySelector('script[src*="oi.linechart.min.js"]') === null) {
    const script = document.createElement('script');
    script.src = 'https://open-innovations.github.io/leeds-2023/js/oi.linechart.min.js';
    script.addEventListener('load', () => document.dispatchEvent(lineChartReady));
    document.head.appendChild(script);
  };
  document.head.querySelector('script[src*="oi.linechart.min.js"]');
}

export default () => {
  return `<script>${ initLineChart.toString() }; initLineChart();</script>`;
}