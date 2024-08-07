import lume from "lume/mod.ts";
import base_path from "lume/plugins/base_path.ts";
import date from "lume/plugins/date.ts";
import esbuild from 'lume/plugins/esbuild.ts';
import imagick from "lume/plugins/imagick.ts";
import inline from "lume/plugins/inline.ts";
import jsx from "lume/plugins/jsx.ts";
import metas from "lume/plugins/metas.ts";
import postcss from "lume/plugins/postcss.ts";
import svgo from "lume/plugins/svgo.ts";
import colorFunction from "npm:postcss-color-function";

import { walkSync } from "std/fs/mod.ts";

import oiViz from 'oi-lume-viz/mod.ts';
import csvLoader from 'oi-lume-utils/loaders/csv-loader.ts';
import jsonLoader from 'lume/core/loaders/json.ts';
import autoDependency from 'oi-lume-utils/processors/auto-dependency.ts';
import * as colours from './docs/_data/colours.js';

import * as filters from 'local/filters.ts';
import getFonts from 'local/oi/get-fonts.ts';

const nunjucks = {
  options: {
    throwOnUndefined: false,
  },
};

const site = lume({
  location: new URL("https://data.leeds2023.co.uk/"),
  src: "./docs",
  components: {
    cssFile: '/assets/css/components.css',
    jsFile: '/assets/js/components.js',
  },
}, {
  nunjucks,
});

// Add dependencies
site.process(['.html'], autoDependency);

// Enforce standard styling of LEEDS 2023
site.process(['.html'], (page) => {
  page.document.body.innerHTML = page.document.body.innerHTML.replace(/leeds\s+2023/gi, 'LEEDS 2023');
});

site.use(base_path());
site.use(imagick());
site.use(inline());
site.use(jsx());
site.use(metas());
site.use(postcss({
  plugins: [colorFunction({ preserveCustomProps: true })],
  keepDefaultPlugins: true,
}));
site.use(esbuild({
  extensions: [".ts", ".js"],
  options: {
    bundle: true,
    format: "iife",
    minify: true,
    keepNames: false,
    platform: "browser",
    target: "es6",
    // incremental: true,
    treeShaking: true,
    logOverride: {
      // This surpresses a warning caused by mermaid. Ideally, I'd like to
      // prevent errors being raised by 3rd party libraries, as we have no
      // control over them.
      'equals-new-object': 'silent',
    },
  },
}));
site.use(date());
site.use(oiViz({
	assetPath: '/assets/oi',
	componentNamespace: 'oi.viz',
	"colour": {
		"names": {
			"mint": colours.mint,
			"darkmint": colours.darkmint,
			"yellow": colours.yellow,
			"darkyellow": colours.darkyellow,
			"magenta": colours.magenta,
			"cyan": colours.cyan,
			"darkcyan": colours.darkcyan,
			"darkmagenta": colours.darkmagenta
		},
		"scales": {
			"mint": colours.mint+' 0%, '+colours.darkmint+' 100%',
			"lightmint": 'rgb(255,255,255) 0%, '+colours.mint+' 100%',
			"yellow": colours.yellow+' 0%, '+colours.darkyellow+' 100%',
			"lightyellow": 'rgb(255,255,255) 0%, '+colours.yellow+' 100%',
			"cyan": colours.cyan+' 0%, '+colours.darkcyan+' 100%',
			"lightcyan": 'rgb(255,255,255) 0%, hsl(173, 100%, 50%) 100%',
			"magenta": colours.magenta+' 0%, '+colours.darkmagenta+' 100%',
			"lightmagenta": 'rgb(255,255,255) 0%, '+colours.magenta+' 100%'
		}
	}
}));
site.use(svgo());

site.loadPages([".html"]);

// Wrap up the CSV loader in some error handling
site.loadData([".csv"], async (filePath) => {
  try {
    const data = await csvLoader(filePath)
    return data;
  } catch(e) {
    if (e.message.match(/^File has no data/)) {
      console.error(e.message);
      return undefined;
    }
    throw e;
  }
});

site.loadData([".geojson"], jsonLoader);


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
site.remoteFile('/js/oi.log.js', 'https://open-innovations.org/resources/oi.log.js');
site.remoteFile('/assets/js/vendors/mermaid.js', 'https://unpkg.com/mermaid@8.8.0/dist/mermaid.js');

site.copy('/js');
site.copy('/assets/images');
site.copy('/assets/js/vendors');

// Publish raw data
Array.from(walkSync('./data/metrics', { includeDirs: false })).forEach(({ path }) => {
  site.remoteFile(`/data/${path.replace(/^data\/metrics\//, "")}`, `./${path}`)
});

[
  'exec_summary_mwmcmn.pdf',
  'mwmcmn_ace.csv',
  'mwmcmn_lcf.csv',
  'description.txt'
].forEach(file => {
  site.remoteFile(`/data/report/mwmcmn/${file}`, `./data/report/mwmcmn/${file}`)
})
site.copy('/data');

// Get Favicon
site.remoteFile('/favicon.ico', 'https://leeds2023.co.uk/favicon.ico');
site.copy('/favicon.ico');

// Get some super tiny icons
site.remoteFile('/assets/images/icons/github.svg', 'https://cdn.jsdelivr.net/gh/edent/SuperTinyIcons@master/images/svg/github.svg');

site.remoteFile('/assets/images/icons/oi.svg', "https://open-innovations.org/resources/images/logos/oi-square-black.svg");
site.copy('/assets/images/icons');

site.copy('.nojekyll');
site.copy('CNAME');

site.filter('localize', (num) => num.toLocaleString())
site.filter('lookup', filters.lookup);
site.filter('getDataByPath', filters.getKey);
site.filter('values', (obj) => Object.values(obj));
/**
 * Converts a number into a more human-friendly number.
 * 
 * Pass a second argument to limit the maximum exponent (1k = 3, 1m = 6 1bn = 9)
 */
site.filter('humanise', (input, max_exponent = Infinity, spacer = '') => {
  const number = parseFloat(input);
  const exponent = Math.min(Math.round(Math.log10(number)), max_exponent);
  if (exponent >= 9) {
    return `${(number / 1e9).toLocaleString()}${spacer}bn`;
  }
  if (exponent >= 6) {
    return `${(number / 1e6).toLocaleString()}${spacer}m`;
  }
  if (exponent >= 3) {
    return `${(number / 1e3).toLocaleString()}${spacer}k`;
  }
  return number.toLocaleString();
});

site.filter('pathUpdated', filters.gitPathUpdated, true);
site.filter('sub', (x, pattern, replacement) => x.replace(pattern, replacement));

export default site;
