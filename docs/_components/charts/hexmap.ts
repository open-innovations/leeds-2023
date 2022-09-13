export const css = `
  .hexmap {
    --hex-fill: var(--l23-cyan);
    background: var(--l23-mint);
    & .hex {
      fill: var(--hex-fill);
      transform: scale(0.95);
      transition: transform 0.1s linear;
      &:hover {
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
  margin: number;
  hexWidth: number;
  titleProp: string;
};

export default function ({
  hexjson,
  margin = 25,
  hexWidth = 100,
  titleProp = 'n',
}: HexmapOptions) {
  const { layout, hexes } = hexjson;

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
    console.log(label);
    return `<g
        transform="translate(${x - qWidth / 2} ${y})"
      >
        <path
          class="hex"
          data-hover="${label}"
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
      </g>`;
  };

  return `<svg
      class="hexmap"
      viewBox="
        ${-margin - hexWidth / 2} ${-margin - hexSide}
        ${width + hexWidth + 2 * margin} ${height +  2 * (margin + hexSide)}
      "
      xmlns="http://www.w3.org/2000/svg"
      xmlns:xlink="http://www.w3.org/1999/xlink"
      data-dependencies="/assets/js/interactive-chart.js"
    >
      ${Object.values(hexes).map(drawHex).join('')}
    </svg>
  `;
}
