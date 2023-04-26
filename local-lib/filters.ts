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

export async function gitPathUpdated(path: string) {
  const p = await Deno.run({ cmd: ["git", "log", "-1", '--pretty="%cI"', "--", path], stdout: 'piped' })
  return new TextDecoder().decode(await p.output()).trim().replace(/"/g, '');
}