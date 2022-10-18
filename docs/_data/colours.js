import { Colour, ColourScale } from 'local/oi/colours.js';

export const scales = {
	'mint': ColourScale('hsl(87, 57%, 86%) 0%, hsl(191, 57%, 15%) 100%'),
	'yellow': ColourScale('hsl(52, 100%, 50%) 0%, hsl(191, 57%, 15%) 100%'),
	'magenta': ColourScale('hsl(321, 100%, 50%) 0%, rgb(0, 0, 0) 100%')
};

//console.log(Colour('hsl(87, 57%, 86%)'));


/*
export const mint = generateSingleColourScale(87, 57);
export const yellow = generateTwoColourScale([52, 100, 50], [52, 100, 15]);

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
*/