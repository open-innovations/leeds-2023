export default ({ label, current, target, sample = false }) => {
  const html = [];
  html.push(`<div class="current-vs-target ${ sample ? 'sample-data' : ''}">`);
  html.push(`<p class="large centred"><span class="current">${ current }</span></p>`)
  if (label) html.push(`<p class="centred">${ label }</p>`)
  html.push(`<p class="centred">target: <span class="target">${ target }</span></p>`)
  html.push('</div>');
  return html.join('');
}

export const css = `
.current-vs-target {
  border: 1px solid grey;
  & .large {
    font-size: 5rem;
    font-weight: 900;
    font-family: var(--title-fontstack);
  }
  & .target {
    font-family: var(--title-fontstack);
  }
  & .centred {
    text-align: center;
  }
  & .sample-data {
    font-style: italic;
    color: rgb(194, 50, 50);
  }
}
`;