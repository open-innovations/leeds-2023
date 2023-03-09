export function lookup(data: Record<string, unknown>[], key: string, entry: string, value: string) {
  const result = data.find(x => x[key] = entry);
  if (result === undefined) throw new ReferenceError('No entry found');
  return result[value];
}

export function getKey(context: Record<string, unknown>, path: string) {
  return path
    .split('.')
    .reduce(
      (result, key) => result[key] as Record<string, unknown>,
      context
    );
}