import lume from "lume/mod.ts";
import base_path from "lume/plugins/base_path.ts";
import date from "lume/plugins/date.ts";
import esbuild from 'lume/plugins/esbuild.ts';
import imagick from "lume/plugins/imagick.ts";
import inline from "lume/plugins/inline.ts";
import jsx from "lume/plugins/jsx.ts";
import metas from "lume/plugins/metas.ts";
import postcss from "lume/plugins/postcss.ts";

import oiCharts from 'oi-lume-charts/mod.ts';
import csvLoader from 'oi-lume-utils/loaders/csv-loader.ts';
import autoDependency from 'oi-lume-utils/processors/auto-dependency.ts';

import getFonts from 'local/oi/get-fonts.ts';

const site = lume({
  location: new URL("https://data.leeds2023.open-innovations.org/"),
  src: "./docs",
  components: {
    cssFile: '/style/components.css'
  }
});

// Add dependencies
site.process(['.html'], autoDependency);

// Enforce standard styling of LEEDS 2023
site.process(['.html'], (page) => {
  page.document.body.innerHTML = page.document.body.innerHTML.replace(/leeds\s+2023/gi, '<span class="leeds-2023-logo">LEEDS 2023</span>');
});

site.use(base_path());
site.use(imagick());
site.use(inline());
site.use(jsx());
site.use(metas());
site.use(postcss());
site.use(esbuild({
  extensions: [".ts", ".js"],
  options: {
    bundle: true,
    format: "iife",
    minify: true,
    keepNames: false,
    platform: "browser",
    target: "es6",
    incremental: true,
    treeShaking: true,
  },
}));
site.use(date());
site.use(oiCharts({
  assetPath: 'assets/oi',
  componentNamespace: 'oi.charts',
}));

site.loadPages([".html"]);

site.loadData([".csv"], csvLoader);

// TODO Get access to the font files
// [
//   'RebondGrotesque-Bold.eot',
//   'RebondGrotesque-Bold.woff2',
//   'RebondGrotesque-Bold.woff',
//   'RebondGrotesque-Medium.eot',
//   'RebondGrotesque-Medium.woff2',
//   'RebondGrotesque-Medium.woff',
// ].forEach(font => {
//   site.remoteFile(`/assets/fonts/${font}`, `https://leeds2023.co.uk/wp-content/themes/leeds2023/assets/fonts/${font}`);
// })

site.script("get-fonts", getFonts);

site.remoteFile('/js/oi.linechart.min.js', 'https://raw.githubusercontent.com/open-innovations/oi.linechart.js/main/oi.linechart.min.js');
site.remoteFile('/assets/js/vendors/mermaid.js', 'https://unpkg.com/mermaid@8.8.0/dist/mermaid.js');

site.copy('/js');
site.copy('/assets/images');
site.copy('/assets/js/vendors');

// Publish raw data
[
  'ballot/ballot_entries.csv',
  'roadshows/attendance_and_communication_signup_summary.csv',
  'roadshows/attendance.csv',
  'social/twitter.csv',
  'social/instagram.csv',
  'social/linkedin.csv',
  'social/facebook.csv'
].forEach(file => {
  site.remoteFile(`/data/${file}`, `./data/metrics/${file}`)
})
site.copy('/data');

[
  'report/exec_summary_report.pdf',
].forEach(file => {
  site.remoteFile(`/data/${file}`, `./data/report/${file}`)
})
site.copy('/data');

// Get Favicon
site.remoteFile('/favicon.ico', 'https://leeds2023.co.uk/favicon.ico');
site.copy('/favicon.ico');

// Get some super tiny icons
site.remoteFile('/assets/images/icons/github.svg', 'https://cdn.jsdelivr.net/gh/edent/SuperTinyIcons@master/images/svg/github.svg');
site.copy('/assets/images/icons');

site.copy('.nojekyll');
site.copy('CNAME');

site.filter('localize', (num) => num.toLocaleString())

export default site;
