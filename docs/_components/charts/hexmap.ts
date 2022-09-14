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

  const hexSide = hexWidth / 2 / Math.cos(Math.PI / 6);
  const rHeight = 1.5 * hexSide;
  const qWidth = hexWidth;
  const width = (dimensions.right.q - dimensions.left.q) * qWidth;
  const height = (dimensions.bottom.r - dimensions.top.r) * rHeight;
  const rOffset = (r: number) => {
    const isEven = r % 2 === 0;
    // Add options for other layouts in here
    if (layout === 'odd-r') return !isEven ? hexWidth / 2 : 0;
    throw 'Unsupported layout';
  };

  function getCentre({ q, r }: HexDefinition) {
    const x = (q - dimensions.left.q) * qWidth + rOffset(r);
    const y = height - (r - dimensions.top.r) * rHeight;
    return { x, y };
  }

  const drawHex = (config: HexDefinition) => {
    const { x, y } = getCentre(config);
    const label = config[titleProp];
    const value = config[valueProp];
    return `<g
          class="hex"
          transform="translate(${x - qWidth / 2} ${y})"
          data-auto-popup="${popup({ label, value })}"
        >
        <path
          style="--hex-fill: ${colourScale(value / maxAttendees)}"
          d="
            M ${qWidth / 2},${-hexSide / 2}
            v ${hexSide}
            l ${-qWidth / 2},${hexSide / 2}
            l ${-qWidth / 2},${-hexSide / 2}
            v ${-hexSide}
            l ${qWidth / 2},${-hexSide / 2}
            Z
          "
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
        ${-margin - hexWidth / 2} ${-margin - hexSide}
        ${width + hexWidth + 2 * margin} ${height + 2 * (margin + hexSide)}
      "
      style="
        {%- if bgColour %}--hex-bg: {{ bgColour }}{% endif -%}
      "
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      data-dependencies="/assets/js/auto-popup.js"
    >
      ${Object.values(hexes).map(drawHex).join('')}
    </svg>
  `;
}
