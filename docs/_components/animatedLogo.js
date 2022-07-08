export default function () {
  return `<section id="big-logo" style="text-align: center;">
  <div>
  <img src='/assets/images/logo.svg' inline/>
  </div>
  <div>
  <button id='animate'>Animate Logo</button>
  </div>
  </section>
<script>
window.addEventListener('DOMContentLoaded', () => {
  const flashSpeed = 100;
  const button = document.querySelector('#big-logo #animate');
  const path = document.querySelector('#big-logo svg g path');
  let blitter;
  const setRandomColour = () => {
    const colour = Math.trunc(Math.random() * 255);
    path.setAttribute('fill', \`hsl(\${colour}, 50%, 50%)\`);
  };
  const startAnimation = () => {
    button.removeEventListener('click', startAnimation);
    blitter = setInterval(setRandomColour, flashSpeed);
    button.innerHTML = 'Stop Retro Loading Animation';
    button.addEventListener('click', stopAnimation);
  }
  const stopAnimation = () => {
    button.removeEventListener('click', stopAnimation);
    clearInterval(blitter);
    button.innerHTML = 'Start Retro Loading Animation';
    button.addEventListener('click', startAnimation);
  }
  stopAnimation();
  button.addEventListener('click', startAnimation);
})
</script>`;
}

export const css = `
#big-logo svg {
  max-width: 100%;
  width: 635px;
}
`;
