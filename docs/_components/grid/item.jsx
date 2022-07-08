export default ({ title, link, summary, id, cls = 'grid-item' }) => <li>
  <a id={id} class={cls} href={link}>
    <h2>{title}</h2>
    <p>{summary}</p>
  </a>
</li>;

export const css = `
.grid-item {
  color: #000;
  background-color: var(--l23-cyan);
  display: block;
  &:hover {
    background-color: #000;
    color: white;
  }
}
`;