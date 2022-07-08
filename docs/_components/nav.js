export default function ({ search, url }) {
  const pages = search.pages('nav_order!=undefined', 'nav_order');
  const links = pages.map(page => `<a ${ url == page.data.url ? 'class="active" ' : '' }href="${ page.data.url }">${ page.data.title }</a>`).join('')

return `<input hidden id="menu-state" class="menu-state" type="checkbox">
<label class="menu-toggle" for="menu-state">
  <div class="menu-burger"><i></i><i></i><i></i></div>
</label>
<nav class="menu-items">${links}</nav>
`;
}