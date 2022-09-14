const POPUP_TIMEOUT = 2500;
const MAX_TIMEOUT = 500;
addEventListener('DOMContentLoaded', () => {
  // Create and attach the popup
  const popup = document.createElement('aside');
  popup.className = 'popup';
  popup.style.display = 'none';
  popup.style.opacity = 0;
  document.body.appendChild(popup);
  let fader: number | undefined = undefined;

  /**
   * Event handler to show the popup.
   * 
   * @param event event target
   */
  function showPopup(event) {
    if (fader) clearTimeout(fader);
    popup.style.display = null;
    console.log(event.target);
    console.log(event.currentTarget);
    popup.innerHTML = event.currentTarget.dataset.hover;
    const loc = event.currentTarget.getBoundingClientRect();
    const hoverPos = event.currentTarget.dataset.hoverPos || 'bottom';
    popup.dataset.hoverPos = hoverPos;
    switch (hoverPos) {
      case 'right':
        popup.style.top = loc.top + loc.height / 2 + 'px';
        popup.style.left = loc.right + 10 + 'px';
        break;
      case 'bottom':
      default:
        popup.style.top = loc.bottom + 10 + 'px';
        popup.style.left = loc.left + loc.width / 2 + 'px';
        break;
    }
    // Do this on the next event (left timeout out!)
    setTimeout(function () {
      popup.style.opacity = 1;
    });
  }
  /**
   * Factory to create an event listener which hides the popup.
   * @param delay - time period to wait before fading
   * @returns 
   */
  function hidePopup(delay = POPUP_TIMEOUT) {
    return function() {
      fader = setTimeout(function () {
        popup.style.opacity = 0;
        setTimeout(function () {
          popup.style.display = 'none';
          fader = undefined;
        }, MAX_TIMEOUT);
      }, delay);
    }
  }

  // Attach listeners
  addEventListener('scroll', hidePopup(0));
  // Get all the hoverable elements
  const hoverables = document.querySelectorAll('[data-hover]');
  for (const hoverable of hoverables) {
    hoverable.addEventListener('mouseover', showPopup);
    hoverable.addEventListener('mouseout', hidePopup());
  }
});
