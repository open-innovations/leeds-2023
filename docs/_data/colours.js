import { Colour, ColourScale } from 'local/oi/colours.js';

export const mint = 'hsl(87, 57%, 86%)';
export const yellow = 'hsl(52, 100%, 50%)';
export const magenta = 'hsl(321, 100%, 50%)';
export const cyan = 'hsl(173, 65%, 61%)';
export const darkcyan = 'hsl(191, 57%, 15%)';

export const scales = {
	'mint': ColourScale(mint+' 0%, '+darkcyan+' 100%'),
	'yellow': ColourScale(yellow+' 0%, '+darkcyan+' 100%'),
	'magenta': ColourScale(magenta+' 0%, rgb(0, 0, 0) 100%')
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