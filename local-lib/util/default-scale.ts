/**
 * Function which returns a sort of cyan colour scaled between completely white (lightness 100%) and
 * full fat colour (50% lightness), based on provided value
 *
 * @param value Value to visualise from 0 to 1, where 1 is coloured and 0 is white
 * @returns 
 */
export const defaultScale = (value = 0) => `hsl(173, 100%, ${100 - value * 50}%)`;
