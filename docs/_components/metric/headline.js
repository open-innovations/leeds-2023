export default function({ comp, metrics, title, value, suffix, description, link, colour, background, headingLevel = 2 }) {
  const content = [
    `<h${headingLevel}>${title}</h${headingLevel}>`,
    comp.viz.bigNumber({ number: value, suffix: suffix }),
    `<p class="tagline">${description}</p>`,
  ];

  return comp.grid.block.impact({
    link: link,
    fg: colour,
    bg: background,
    content: content.join('')
  });
  
}