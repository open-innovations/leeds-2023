export const css = `
.ward-graphic {
  --ward-size: 13vw;
  --row-offset: calc(var(--ward-size) * -0.5);
  --row-height: calc(var(--ward-size) * 0.866);
  padding-block-end: 2vw;
  & * {
    margin-top: 0;
  }
  & .row {
    display: flex;
    position: relative;
    height: var(--row-height);
    &:nth-child(2n) {
      position: relative;
      left: var(--row-offset);
    }
  }
  & .hex {
    width: var(--ward-size);
    aspect-ratio: 1 / 1;
    transition: scale 0.5s, z-index 0.5s;
    &:hover {
      scale: 1.1;
      z-index: 10;
    }
    &.empty {
      visibility: hidden;
    }
  }
}
`;

function transpose(a) {
  return Object.keys(a[0]).map(function(c) {
      return a.map(function(r) { return r[c]; });
  });
}
function calculateMinMax(layout) {
  const coordinates = transpose(Object.values(layout.hexes).map(({q, r}) => [q, r]));
  const res =  {
    q: {
      min: Math.min(...coordinates[0]),
      max: Math.max(...coordinates[0])
    },
    r: {
      min: Math.min(...coordinates[1]),
      max: Math.max(...coordinates[1])
    }
  }
  res.q.count = res.q.max - res.q.min;
  res.r.count = res.r.max - res.r.min;

  return res;  
}

export default function({ hex }) {
  const layout = hex.wards_leeds;
  const ranges = calculateMinMax(layout);

  function getContent(r, q) {
    const hex = Object.entries(layout.hexes).find(h => h[1].q === q && h[1].r === r);
    return hex;
  }

  const rows = [];
  function generateQolumns(r: number) {
    const qolumns = []
    for (let q = ranges.q.min; q <= ranges.q.max; q++) {
      const content = getContent(r, q);
      if (!content) {
        qolumns.push(`<div class='hex empty'></div>`)
        continue;
      }
      const name = content[1].n;
      const codename = name.toLowerCase().replace(/[^\w]+/g, '-').replace(/(and-)/g, '')
      qolumns.push(`<div class='hex'><img title="${name}" tabindex=1 src="/assets/images/the-gift/${codename}.png"></div>`)
    }
    return qolumns;
  }
  for (let r = ranges.r.max; r >= ranges.r.min; r--) {
    rows.push(`<div class='row'>${generateQolumns(r).join('')}</div>`)
  }

  return `<div class='ward-graphic'>${rows.join('')}</div>`
}