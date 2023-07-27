import { ColourScale } from 'local/oi/colours.js';

export const mint = '#ddf0c7';
export const darkmint = '#365016';
export const yellow = '#ffdd00';
export const darkyellow = '#665800';
export const magenta = '#ff00a6';
export const cyan = '#5bdccd';
export const darkcyan = '#10343c';
export const darkmagenta = '#5e0e37';
export const darkbluegrey =  '#00353d';

export const scales = {
	'mint': ColourScale(mint+' 0%, '+darkmint+' 100%'),
	'yellow': ColourScale(yellow+' 0%, '+darkyellow+' 100%'),
	'cyan': ColourScale(cyan+' 0%, '+darkcyan+' 100%'),
	'magenta': ColourScale(magenta+' 0%, '+darkmagenta+' 100%')
};
