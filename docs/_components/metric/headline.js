export default function({ comp, metrics, title, value, description, link, colour, background, headingLevel = 2 }) {
  const content = [
    `<h${headingLevel}>${title}</h${headingLevel}>`,
    comp.viz.bigNumber({ number: value }),
    `<p>${description}</p>`,
  ];
  console.log(background, colour)

  return comp.grid.block.impact({
    link: link,
    fg: colour,
    bg: background,
    content: content.join('')
  });
  
}