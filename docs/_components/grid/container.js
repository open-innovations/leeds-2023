export default ({ content }) => {
  return `<ul class="grid">${ content }</ul>`;
}

export const css = `
.grid {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 1em;
  grid-auto-rows: auto;
  grid-template-columns: 100%;
  
  @media screen and (min-width: 800px) {
    grid-template-columns: repeat(3,minmax(0,1fr));
  }
  
  & li {
    display: block;
  }
  
}
`;