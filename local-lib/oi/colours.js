/**
	Colours v0.4.0

	A Colour object can be created with:

		Colour('hsl(50, 50%, 78%)')
		Colour('rgb(255, 200, 22)')
		Colour('#ffdd22')

	A Colour contains:
		Colour.rgb - RGB e.g. [0,0,0]
		Colour.hex - a hex code e.g. '#000000'
		Colour.hsl - HSL e.g. 'hsl(0,0,0)'
		Colour.contrast - the most contrasting colour e.g. 'white'

	A ColourScale function can be created with:

		ColourScale('hsl(87, 57%, 86%) 0%, hsl(191, 57%, 15%) 100%')

	The ColourScale object will, by default, return a colour given a 
	value in the range 0 to 1. It is also possible to return:
	
		ColourScale.orig - the original colour stops string
		ColourScale.gradient - a string for the CSS linear gradient
 **/
export function Colour(str){ return new C(str); }
function C(str){
  // Parse the string
  let rgb = [0,0,0];
  let hex = '#000000';
  let hsl = [0,0,0];
  let contrast = 'white';
  
  if(str.indexOf('hsl')==0){
	str = str.replace(/hsl\(/,"").replace(/\)/,"");
	var bits = str.split(/,/);
	for(var i = 0; i < bits.length; i++) bits[i] = parseInt(bits[i]);
	hsl = bits;
	rgb = hslToRgb(hsl[0],hsl[1],hsl[2]);
	hex = hslToHex(hsl[0],hsl[1],hsl[2]);
  }else if(str.indexOf('rgb')==0){
	str = str.replace(/rgba?\(/,"").replace(/\)/,"");
	var bits = str.split(/,/);
	for(var i = 0; i < bits.length; i++) bits[i] = parseInt(bits[i]);
	rgb = bits;
	hsl = rgbToHsl(rgb[0],rgb[1],rgb[2]);
	hex = rgbToHex(rgb[0],rgb[1],rgb[2]);
  }else if(str.indexOf('#')==0){
	hex = str;
	rgb = hexToRGB(hex);
	hsl = rgbToHsl(rgb[0],rgb[1],rgb[2]);
  }
  
  // Check brightness contrast
  let cols = {'black':{'rgb':[0,0,0]},'white':{'rgb':[255,255,255]}};
  let col;
  for(col in cols){
	cols[col].brightness = brightnessDiff(rgb,cols[col].rgb);
	cols[col].hue = hueDiff(rgb,cols[col].rgb);
	cols[col].ok = (cols[col].brightness > 125 && cols[col].hue >= 500);
  }
  for(col in cols){
	if(cols[col].ok) contrast = 'rgb('+cols[col].rgb.join(",")+')';
  }
  contrast = (cols.white.brightness > cols.black.brightness) ? "white" : "black";
  
  return { rgb, hex, hsl, contrast };
}
function rgbToHsl(r, g, b){
    r /= 255, g /= 255, b /= 255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var h, s, l = (max + min) / 2;

    if(max == min){
        h = s = 0; // achromatic
    }else{
        var d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch(max){
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }

    return [Math.floor(h * 360), Math.floor(s * 100), Math.floor(l * 100)];
}
function hslToHex(h, s, l) {
	l /= 100;
	const a = s * Math.min(l, 1 - l) / 100;
	const f = n => {
		const k = (n + h / 30) % 12;
		const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
		return Math.round(255 * color).toString(16).padStart(2, '0');   // convert to Hex and prefix "0" if needed
	};
	return `#${f(0)}${f(8)}${f(4)}`;
}
function hslToRgb(h,s,l){
	l /= 100;
	let a = s*Math.min(l,1-l) / 100;
	let f = (n,k=(n+h/30)%12) => l - a*Math.max(Math.min(k-3,9-k,1),-1);
	return [Math.round(255*f(0)),Math.round(255*f(8)),Math.round(255*f(4))];
}
function rgbToHex(r, g, b){
	return '#'+d2h(r)+d2h(g)+d2h(b);
}
function hexToRGB(hex){
	return [h2d(hex.substring(1,3)), h2d(hex.substring(3,5)), h2d(hex.substring(5,7))];
}
function d2h(d) { return ((d < 16) ? "0" : "") + d.toString(16); }
function h2d(h) { return parseInt(h, 16); }
function brightnessIndex(rgb){ return rgb[0]*0.299 + rgb[1]*0.587 + rgb[2]*0.114; }
function brightnessDiff(a,b){ return Math.abs(brightnessIndex(a)-brightnessIndex(b)); }
function hueDiff(a,b){ return Math.abs(a[0]-b[0]) + Math.abs(a[1]-b[1]) + Math.abs(a[2]-b[2]); }
export function ColourScale(grad){ return new CS(grad); }
function CS(grad) {

	function col(a) {
		if (typeof a === "string") return Colour(a);
		else return a;
	}

	function extractColours(str) {
		var stops, cs, i, c;
		stops = str.match(/(([a-z]{3,4}\([^\)]+\)|#[A-Fa-f0-9]{6}) \d+\%?)/g);
		cs = [];
		for (i = 0; i < stops.length; i++) {
			var v = '';
			stops[i].replace(/ (\d+\%?)$/,function(m,p1){ v = p1; return ''; });
			var bits = stops[i].split(/ /);
			cs.push({ 'v': v, 'c': Colour(stops[i]) });
		}

		for (c = 0; c < cs.length; c++) {
			if (cs[c].v) {
				// If a colour-stop has a percentage value provided, 
				if (cs[c].v.indexOf('%') >= 0) cs[c].aspercent = true;
				cs[c].v = parseFloat(cs[c].v);
			}
		}
		return cs;
	}

	let min = 0;
	let max = 1;
	let stops = extractColours(grad);

	function getColourPercent(pc, a, b, inParts) {
		pc /= 100;
		if(typeof inParts!=="boolean") inParts = false;
		if(typeof a.alpha!=="number") a.alpha = 1;
		if(typeof b.alpha!=="number") b.alpha = 1;
		let c = {
			'r': parseInt(a.rgb[0] + (b.rgb[0] - a.rgb[0]) * pc),
			'g': parseInt(a.rgb[1] + (b.rgb[1] - a.rgb[1]) * pc),
			'b': parseInt(a.rgb[2] + (b.rgb[2] - a.rgb[2]) * pc),
			'alpha': ((b.alpha - a.alpha) * pc + a.alpha)
		};
		if (inParts) return c;
		else return 'rgb' + (c.alpha && c.alpha < 1 ? 'a' : '') + '(' + c.r + ',' + c.g + ',' + c.b + (c.alpha && c.alpha < 1 ? ',' + c.alpha : '') + ')';
	};

	function getColour(v){
		var v2, pc, c, cfinal;
		v2 = 100 * (v - min) / (max - min);
		cfinal = {};
		if (v == max) cfinal = { 'r': stops[stops.length - 1].c.rgb[0], 'g': stops[stops.length - 1].c.rgb[1], 'b': stops[stops.length - 1].c.rgb[2], 'alpha': stops[stops.length - 1].c.alpha };
		else {
			if (stops.length == 1) cfinal = { 'r': stops[0].c.rgb[0], 'g': stops[0].c.rgb[1], 'b': stops[0].c.rgb[2], 'alpha': (v2 / 100).toFixed(3) };
			else {
				for (c = 0; c < stops.length - 1; c++) {
					if (v2 >= stops[c].v && v2 <= stops[c + 1].v) {
						// On this colour stop
						pc = 100 * (v2 - stops[c].v) / (stops[c + 1].v - stops[c].v);
						if (pc > 100) pc = 100;	// Don't go above colour range
						cfinal = getColourPercent(pc, stops[c].c, stops[c + 1].c, true);
						continue;
					}
				}
			}
		}

		// If no red value is set and the value is greater than the max value, we'll default to the max colour
		if(typeof cfinal.r!=="number" && v > max) cfinal = { 'r': stops[stops.length - 1].c.rgb[0], 'g': stops[stops.length - 1].c.rgb[1], 'b': stops[stops.length - 1].c.rgb[2], 'alpha': stops[stops.length - 1].c.alpha };

		return 'rgba(' + cfinal.r + ',' + cfinal.g + ',' + cfinal.b + ',' + cfinal.alpha + ")";
		
	}
	const fn = getColour;
	fn.orig = grad;
	fn.gradient = 'background: -moz-linear-gradient(left, ' + grad + ');background: -webkit-linear-gradient(left, ' + grad + ');background: linear-gradient(to right, ' + grad + ');';
	
	return fn;
}
/* END OF COLOUR FUNCTIONS */
