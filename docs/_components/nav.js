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
    <input hidden id="menu-state" class="menu-state" type="checkbox">
    <label class="menu-toggle" for="menu-state">
      <div class="menu-burger"><i></i><i></i><i></i></div>
    </label>
    <ul class="menu-items">${links}</ul>
  </nav>`;
}

export const css = `
.menu-state {
  display: none;
}

.menu-toggle {
  @media screen and (min-width: 800px) {
    display: none;
  }

  @nest .menu-state:checked ~ & {
    /* transform: translateY(var(--header-height)); */
    & .menu-burger {
      & i:nth-of-type(1) {
        transform: translateY(0.7rem) scaleX(0);
      }
      & i:nth-of-type(2) {
        transform: rotate(225deg) scale(1.41);
      }
      & i:nth-of-type(3) {
        transform: translateY(-0.7rem) rotate(135deg) scale(1.41);
      }
    }
  }
}

.menu-burger {
  width: 1.8rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 0.4rem;

  & i {
    height: 0.3rem;
    background-color: black;
    transition: ease transform 250ms;
    border-radius: 0.8rem;
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
  transition: 250ms ease;
  transition-property: left, right;

  @media screen and (min-width: 800px) {
    flex-direction: row;
    gap: 1em;
    position: unset;
    padding: unset;
    border: unset;
  }
  @nest .menu-state:checked ~ & {
    left: 0;
    right: 0;
  }
}
`;
