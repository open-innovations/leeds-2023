const POPUP_TIMEOUT = 2500;
const MAX_TIMEOUT = 500;
addEventListener('DOMContentLoaded', () => {
  // Create and attach the popup
  const popup = document.createElement('aside');
  popup.className = 'popup';
  popup.style.display = 'none';
  popup.style.opacity = 0;
  document.body.appendChild(popup);

  // Create variables to hold the target and fader
  let target = undefined;
  let fader: number | undefined = undefined;

  /**
   * Event handler to show the popup.
   * 
   * @param event event target
   */
  function showPopup(event) {
    // Clear any fades
    if (fader) clearTimeout(fader);

    // Stop if already focussed on this element
    if (target === event.currentTarget) return;

    // Show the popup
    popup.style.display = null;

    // Capture target triggering the popup
    target = event.currentTarget;

    // Get the location of the target
    const loc = target.getBoundingClientRect();

    // Get the hover position
    const autoPopupPos = target.dataset.autoPopupPos || 'bottom';
    console.log(autoPopupPos);

    // Setup the content and attributes of the popup
    popup.innerHTML = target.dataset.autoPopup;
    popup.dataset.autoPopupPos = autoPopupPos;

    // Set the position of the popup based on requested popup position
    switch (autoPopupPos) {
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

    // Do this on the next click (timeout excluded on purpose!)
    // This enables any change in visibility to take place before animating opacity
    setTimeout(function () {
      // Set the popup opacity to visible
      popup.style.opacity = 1;
    });
  }
  /**
   * Factory to create an event listener which hides the popup.
   * 
   * @param delay - time period to wait before fading
   * @returns 
   */
  function hidePopup(delay = POPUP_TIMEOUT) {
    return function() {
      // Create a fader which hides the popup, after a delay
      fader = setTimeout(function () {
        // Fade the opacity
        popup.style.opacity = 0;
        // Set a timeout to reset everything else
        setTimeout(function () {
          popup.style.display = 'none';
          fader = undefined;
          target = undefined;
        }, MAX_TIMEOUT);
      }, delay);
    }
  }

  // Attach listeners
  addEventListener('scroll', hidePopup(0));
  // Get all the hoverable elements
  const hoverables = document.querySelectorAll('[data-auto-popup]');
  for (const hoverable of hoverables) {
    hoverable.addEventListener('mouseover', showPopup);
    hoverable.addEventListener('mouseout', hidePopup());
  }
});
