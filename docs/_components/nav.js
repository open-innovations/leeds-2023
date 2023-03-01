export default function ({ search, url }) {
  const pages = search.pages('nav_order!=undefined', 'nav_order');
  const links = pages
    .map(
      (page) =>
        `<li><a ${url == page.data.url ? 'class="active" ' : ''}href="${
          page.data.url
        }">${page.data.title}</a></li>`
    )
    .join('');
  
  return `<nav>
    <button aria-expanded="false" class="menu-toggle"><span>Menu</span></button>
    <ul class="menu-items" hidden>${links}</ul>
  </nav>`;
}

export const js = `
  addEventListener('DOMContentLoaded', () => {
    var navButton = document.querySelector('nav button.menu-toggle');
    console.log(navButton);
    navButton.addEventListener('click', function() {
      let expanded = this.getAttribute('aria-expanded') === 'true' || false;
      this.setAttribute('aria-expanded', !expanded);
      let menu = this.nextElementSibling;
      menu.hidden = !menu.hidden;
    });
  });
`

export const css = `
[hidden] {
  display: none;
}

nav {
  --transition-timing: 250ms linear;
}

.menu-toggle {
  color: inherit;
  background: unset;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  &:hover span {
    text-decoration: underline;
  }
  &:after {
    content: "\u25C0";
    display: block;
    transition: var(--transition-timing);
    transition-property: transform;
    font-size: 0.5em;
  }
  &[aria-expanded=true]:after {
    transform: rotate(-180deg);
  }
  @media screen and (min-width: 800px) {
    display: none;
  }
}

.menu-items {
  position: absolute;
  top: var(--header-height);
  margin: 0;
  left: 100%;
  right: -100%;
  display: flex;
  flex-direction: column;
  padding: 1em;
  transition: var(--transition-timing);
  transition-property: left, right;
  @nest .menu-toggle[aria-expanded=true] ~ & {
    left: 0;
    right: 0;
  }
  @media screen and (min-width: 800px) {
    flex-direction: row;
    gap: 1em;
    position: unset;
    padding: unset;
    border: unset;
  }
}
`;
