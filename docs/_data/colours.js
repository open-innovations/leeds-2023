import { ColourScale } from 'local/oi/colours.js';

export const mint = 'hsl(87, 57%, 86%)';
export const darkmint = 'hsl(87, 57%, 20%)';
export const yellow = 'hsl(52, 100%, 50%)';
export const darkyellow = 'hsl(52, 100%, 20%)';
export const magenta = 'hsl(321, 100%, 50%)';
export const cyan = 'hsl(173, 65%, 61%)';
export const darkcyan = 'hsl(191, 57%, 15%)';
export const darkmagenta = 'rgb(94, 14, 55)';

export const scales = {
	'mint': ColourScale(mint+' 0%, '+darkmint+' 100%'),
	'yellow': ColourScale(yellow+' 0%, '+darkyellow+' 100%'),
	'cyan': ColourScale(cyan+' 0%, '+darkcyan+' 100%'),
	'magenta': ColourScale(magenta+' 0%, '+darkmagenta+' 100%')
};
