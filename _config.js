import lume from "lume/mod.ts";
import base_path from "lume/plugins/base_path.ts";
import imagick from "lume/plugins/imagick.ts";
import inline from "lume/plugins/inline.ts";
import jsx from "lume/plugins/jsx.ts";
import metas from "lume/plugins/metas.ts";
import postcss from "lume/plugins/postcss.ts";
import { parse as parseCsv } from 'std/encoding/csv.ts';

const site = lume({
  location: new URL("https://open-innovations.github.io/leeds-2023/"),
  src: "./docs",
  components: {
    cssFile: '/style/components.css'
  }
});

site.use(base_path());
site.use(imagick());
site.use(inline());
site.use(jsx());
site.use(metas());
site.use(postcss());

site.loadPages([".html"]);

async function csvLoader(path) {
  const content = await parseCsv(await Deno.readTextFile(path), {
    skipFirstRow: true,
  });
  return { rows: content };
}
site.loadData([".csv"], csvLoader);

[
  'RebondGrotesque-Bold.eot',
  'RebondGrotesque-Bold.woff2',
  'RebondGrotesque-Bold.woff',
  'RebondGrotesque-Medium.eot',
  'RebondGrotesque-Medium.woff2',
  'RebondGrotesque-Medium.woff',
].forEach(font => {
  site.remoteFile(`/assets/fonts/${font}`, `https://leeds2023.co.uk/wp-content/themes/leeds2023/assets/fonts/${font}`);
})

site.remoteFile('/js/oi.linechart.min.js', 'https://raw.githubusercontent.com/open-innovations/oi.linechart.js/main/oi.linechart.min.js');
site.remoteFile('/js/oi.hexmap.min.js', 'https://raw.githubusercontent.com/odileeds/odi.hexmap.js/main/odi.hexmap.min.js');
site.copy('/js');
site.copy('/assets');

site.copy('.nojekyll');

export default site;
