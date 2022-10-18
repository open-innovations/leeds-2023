export const mint = generateSingleColourScale(87, 57)
export const yellow = generateTwoColourScale([52, 100, 50], [52, 100, 15])

function generateSingleColourScale(hue, saturation, startLightness=86, endLightness=50) {
  return function(value) {
    const s = [hue, saturation, startLightness];
    const e = [hue, saturation, endLightness];
    return `hsl(
      ${((e[0] - s[0]) * value ) + s[0]},
      ${((e[1] - s[1]) * value ) + s[1]}%,
      ${((e[2] - s[2]) * value ) + s[2]}%
    )`;
  } 
}

function generateTwoColourScale(startHsl, endHsl) {
  return function(value) {
    return `hsl(
      ${((endHsl[0] - startHsl[0]) * value ) + startHsl[0]},
      ${((endHsl[1] - startHsl[1]) * value ) + startHsl[1]}%,
      ${((endHsl[2] - startHsl[2]) * value ) + startHsl[2]}%
    )`;

  }
}