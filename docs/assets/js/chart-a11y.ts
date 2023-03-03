let currentChart = 0;

function hexes() {
  const hexmaps = document.querySelectorAll('svg.hexmap');
  hexmaps.forEach((hexmap) => {
    addSkipLinks(hexmap);
    const targets = hexmap.querySelectorAll('g.hex');
    targets.forEach(makeTabbable);
  });
}

function makeTabbable(target: Element) {
  target.setAttribute('tabindex', '0');
}
function addSkipLinks(target: Element) {
  const container = target.parentElement;
  if (container === null) return;

  const skipDown = document.createElement('a');
  skipDown.id = 'chart-top-' + currentChart;
  skipDown.href = '#chart-bottom-' + currentChart;
  skipDown.text = 'Skip to bottom of chart';
  target.before(skipDown);

  const skipUp = document.createElement('a');
  skipUp.id = 'chart-bottom-' + currentChart;
  skipUp.href = '#chart-top-' + currentChart;
  skipUp.text = 'Skip to top of chart';
  target.after(skipUp);

  currentChart++;
}

addEventListener('DOMContentLoaded', () => {
  hexes();
});