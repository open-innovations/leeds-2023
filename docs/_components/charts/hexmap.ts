export const css = `
  .hexmap {
    --hex-bg: none;
    --hex-fill: var(--l23-cyan);
    background: var(--hex-bg);
    & .hex {
      & path {
        fill: var(--hex-fill);
        transform: scale(0.95);
        transition: transform 0.1s linear;
      }
      &:hover path {
        transform: scale(0.90);
      }
    }
  }
`;

/**
 *
 * @param options HexmapOptions
 */
type HexDefinition = {
  q: number;
  r: number;
  n: string;
};

type HexmapOptions = {
  hexjson: { layout: string; hexes: Record<string, HexDefinition> };
  data?: Record<string, unknown>[];
  matchKey?: string;
  margin: number;
  hexWidth: number;
  titleProp: string;
  valueProp: string;
  popup: (params: Record<string, string | number>) => string;
  colourScale: (value: number) => string;
  labelProcessor: (label: string) => string;
  bgColour: string;
};

function deepClone<T>(o: T): T {
  return JSON.parse(JSON.stringify(o));
}

const defaultScale = (value = 0) => `hsl(173, 100%, ${100 - value * 50}%)`;

export default function ({
  hexjson,
  data,
  matchKey,
  margin = 10,
  hexWidth = 40,
  titleProp = 'n',
  valueProp,
  popup = ({ label, value }) => `${label}: ${value}`,
  colourScale = defaultScale,
  labelProcessor = (label) => label.slice(0, 3),
  bgColour = 'none',
}: HexmapOptions) {
  const layout = hexjson.layout;
  const hexes = deepClone(hexjson.hexes);

  if (matchKey && data) {
    data.forEach((record) => {
      const key = record[matchKey] as string;
      if (!(key in hexes)) return;
      hexes[key] = { ...hexes[key], ...record };
    });
  }

  const maxAttendees = Object.values(hexes)
    .map((h) => parseFloat(h[valueProp]))
    .reduce((result, current) => Math.max(result, current), 0);

  const dimensions = Object.values(hexes)
    .map(({ q, r }) => ({ q, r }))
    .reduce(
      ({ left, right, top, bottom }, { q, r }) => ({
        left: q < left.q ? { q, r } : left,
        right: q > right.q ? { q, r } : right,
        top: r < top.r ? { q, r } : top,
        bottom: r > bottom.r ? { q, r } : bottom,
      }),
      {
        left: { q: Infinity, r: 0 },
        right: { q: -Infinity, r: 0 },
        top: { q: 0, r: Infinity },
        bottom: { q: 0, r: -Infinity },
      }
    );

  // Length of side = width * tan(30deg)
  const hexSide = hexWidth * Math.tan(Math.PI / 6);

  // Calculate row height and quolum width
  let rHeight: number;
  let qWidth: number;
  switch(layout) {
    case 'odd-r':
    case 'even-r':
      // Row height is 1 and a half - there is a half a side length overlap
      rHeight = 1.5 * hexSide;
      // Column width is set by the hexWidth for point top hexes
      qWidth = hexWidth;
      break;
    case 'odd-q':
    case 'even-q':
      rHeight = hexWidth / 2;
      qWidth = 3 * hexSide;
      break;
    default:
      throw 'Unsupported layout';
  }

  // Overall width of svg (from centre of left-most to centre of right-most)
  const width = (dimensions.right.q - dimensions.left.q) * qWidth;

  // Overall height of svg (from centre of top-most to centre of bottom-most)
  const height = (dimensions.bottom.r - dimensions.top.r) * rHeight;

  /**
   * Calculate the row offset given the prevailing layout
   * 
   * @param r row to calculate offset for
   * @returns 
   */
  const rOffset = (r: number) => {
    const isEven = r % 2 === 0;
    const rLeftMostEven = dimensions.left.r % 2 === 0;
    let shim = 0;
    switch (layout) {
      case 'odd-r':
      case 'odd-q':
        shim = rLeftMostEven ? 0 : qWidth / 2;
        break;
      case 'even-r':
      case 'even-q':
        shim = rLeftMostEven ? qWidth / 2 : 0;
        break;
    }
    const offsetSize = (qWidth / 2);
    let offset = 0;
    if (layout === 'odd-r') offset = isEven ? 0 : offsetSize;
    if (layout === 'even-r') offset = isEven ? offsetSize : 0;
    if (layout === 'odd-q') offset = isEven ? 0 : offsetSize;
    if (layout === 'even-q') offset = isEven ? offsetSize : 0;
    return offset - shim;
  };

  /**
   * Calculate the centre of a hex given a q and r value.
   * 
   * Uses rOffset formula to decide which to shift
   * 
   * @param hexConfig - { q: number, r: number }
   * @returns 
   */
  function getCentre({ q, r }: HexDefinition) {
    const x = (q - dimensions.left.q) * qWidth + rOffset(r);
    const y = height - (r - dimensions.top.r) * rHeight;
    return { x, y };
  }

  const drawHex = (config: HexDefinition) => {
    const { x, y } = getCentre(config);
    const label = config[titleProp];
    const value = config[valueProp];

    // Calculate the path based on the layout
    let hexPath = undefined;
    switch (layout) {
      case 'odd-r':
      case 'even-r':
        hexPath = `
          M ${hexWidth/2},${-hexSide / 2}
          v ${hexSide}
          l ${-qWidth / 2},${hexSide / 2}
          l ${-qWidth / 2},${-hexSide / 2}
          v ${-hexSide}
          l ${qWidth / 2},${-hexSide / 2}
          Z
        `;
        break;
      case 'odd-q':
      case 'even-q':
          hexPath = `
          M ${-hexSide / 2},${ -hexWidth / 2}
          h ${hexSide}
          l ${hexSide / 2},${hexWidth / 2}
          l ${-hexSide / 2},${hexWidth / 2}
          h ${-hexSide }
          l ${-hexSide / 2 },${-hexWidth / 2}
          Z
        `;
        break;
      default:
        throw 'Unsupported layout';
    }

    // TODO this only supports pointy-top hexes at the moment
    return `<g
          class="hex"
          transform="translate(${x} ${y})"
          data-auto-popup="${popup({ label, value })}"
        >
        <path
          style="--hex-fill: ${colourScale(value / maxAttendees)}"
          d="${hexPath}"
        />
        <text
          text-anchor="middle"
          dominant-baseline="middle"
          >${labelProcessor(label)}</text>
      </g>`;
  };

  return `<svg
      class="hexmap"
      viewBox="
        ${ - margin - qWidth / 2} ${ - margin - rHeight / 2}
        ${ width + qWidth + 2 * margin} ${height + rHeight + 2 * margin }
      "
      style="${ bgColour ? `--hex-bg: ${ bgColour }` : ''}"
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      data-dependencies="/assets/js/auto-popup.js"
    >
      ${Object.values(hexes).map(drawHex).join('')}
    </svg>
  `;
}
