/**
 * One-liner to clone an object using the stringigy->parse method.
 * @param o Object to clone
 * @returns 
 */
export const deepClone = <T>(o: T): T => JSON.parse(JSON.stringify(o));
