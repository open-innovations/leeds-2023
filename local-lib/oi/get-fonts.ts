import {
  DOMParser,
  Element,
} from 'https://deno.land/x/deno_dom/deno-dom-wasm.ts';
import { parse, AST, Rule } from 'https://deno.land/x/css@0.3.0/mod.ts';

async function findStylesheets(url: URL) {
  const request = await fetch(url.toString());
  const text = await request.text();
  const document = new DOMParser().parseFromString(text, 'text/html');

  if (document === null) return [];

  return Array.from(document.querySelectorAll('link[rel=stylesheet]'))
    .map((x): string => (<Element>x).getAttribute('href') || '');
}

function getStylesheets(stylesheets: string[], base: URL): Promise<string> {
  return Promise.all(
    stylesheets.map(async (x) => {
      if (x === null) return;
      const cssUrl = new URL(x, base);
      const request = await fetch(cssUrl.toString());
      const css = await request.text();
      return css;
    })
  ).then((result) => result.filter(x => x).join(''));
}

function getFontRules(stylesheets: string, base: URL) {
  const css: AST = parse(stylesheets);
  const fonts: Rule[] = css.stylesheet.rules.filter((x: Rule) => x.type === 'font-face');

  const processValue = (v: string) => v.replace(/url\(\//g, `url\(${base}`);
  const fontCss = fonts
    .map((f) => {
      const rule: string[] = [];
      rule.push('@font-face {');
      rule.push(
        ...f.declarations
          .filter(({ type }) => type === 'property')
          .map(
            ({ name, value }) => {
              if (!value) return '';
              return `  ${name}: ${processValue(value)};`;
            }
          )
      );
      rule.push('}');
      return rule.join('\n');
    })
    .join('\n');
  return fontCss;
}

export default async function getFonts () {
  const url = new URL('https://leeds2023.co.uk');
  const hrefs = await findStylesheets(url);
  const rawCss = await getStylesheets(hrefs, url);
  const fontRules = getFontRules(rawCss, url);
  await Deno.writeTextFile("./docs/_includes/css/fonts.css", fontRules);
}
