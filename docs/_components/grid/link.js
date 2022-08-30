export default ({ title, link, workInProgress = false, summary, id, cls = '', comp }) => `<div>
  <a id=${id} class='grid-link ${cls}' href=${link}>
    <h2>${title}</h2>
    ${ summary && `<p>${summary}</p>` || '' }
    ${ workInProgress && comp.wip_marker({
      bg: 'var(--l23-yellow)',
      fg: 'black',
    }) || '' }
  </a>
</div>`;

export const css = `
.grid-link {
  color: #000;
  background-color: var(--l23-cyan);
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  padding: 1.5em;
  text-decoration: none;
  transition: background-color 0.3s ease-in,color 0.3s ease-in,background 0.3s ease-in;
  &:hover {
    background-color: #000;
    color: white;
  }
  & > :first-child {
    margin-top: 0;
  }
  & > :last-child {
    margin-bottom: 0;
  }
}
`;