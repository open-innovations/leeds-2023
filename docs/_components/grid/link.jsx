export default ({ title, link, summary, id, cls = '' }) => <div>
  <a id={id} class={`grid-link ${cls}`} href={link}>
    <h2>{title}</h2>
    <p>{summary}</p>
  </a>
</div>;

export const css = `
.grid-link {
  color: #000;
  background-color: var(--l23-cyan);
  box-sizing: border-box;
  display: block;
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
    padding-top: 0;
  }
  & > :last-child {
    margin-bottom: 0;
    padding-bottom: 0;
  }
}
`;