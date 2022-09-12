(() => {
  const POPUP_TIMEOUT = 2500;
  const MAX_TIMEOUT = 500;
  addEventListener('DOMContentLoaded', () => {
    const hoverables = document.querySelectorAll('[data-hover]');
    const popup = document.createElement('aside');
    popup.className = 'popup';
    popup.style.display = 'none';
    popup.style.opacity = 0;
    document.body.appendChild(popup);
    let fader = undefined;
    function showPopup({ target }) {
      if (fader) clearTimeout(fader);
      popup.style.display = null;
      popup.innerHTML = target.dataset.hover;
      const loc = target.getBoundingClientRect();
      const size = popup.getBoundingClientRect();
      const hoverPos = target.dataset.hoverPos || 'bottom';
      popup.dataset.hoverPos = hoverPos;
      switch (hoverPos) {
        case 'right':
          popup.style.top = (loc.top + (loc.height - size.height) / 2) + 'px';
          popup.style.left = loc.right + 10 + 'px';
          break;
        case 'bottom':
        default:
          popup.style.top = loc.bottom + 10 + 'px';
          popup.style.left = (loc.x + (loc.width - size.width) / 2) + 'px';
          break;
      }
      // Do this on the next event (left timeout out!)
      setTimeout(function () {
        popup.style.opacity = 1;
      });
    }
    function hidePopup() {
      fader = setTimeout(function () {
        popup.style.opacity = 0;
        setTimeout(function () {
          popup.style.display = 'none';
          fader = undefined;
        }, MAX_TIMEOUT)
      }, POPUP_TIMEOUT);
    }
    for (const hoverable of hoverables) {
      hoverable.addEventListener('mouseover', showPopup);
      hoverable.addEventListener('mouseout', hidePopup);
    }
  });
})();