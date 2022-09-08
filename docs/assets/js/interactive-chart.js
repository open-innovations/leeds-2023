(() => {
  addEventListener('DOMContentLoaded', () => {
    const hoverables = document.querySelectorAll('[data-hover]');
    const popup = document.createElement('div');
    function showPopup({ target }) {
      console.log(target);
      const loc = target.getBoundingClientRect();
      console.log(loc);
    }
    for (const hoverable of hoverables) {
      hoverable.addEventListener('mouseover', showPopup);
    }
  });
})();