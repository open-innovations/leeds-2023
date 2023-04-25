const files = [
  'data/metrics/volunteers/shifts.csv',
  'data/metrics/volunteers/volunteers.csv',
]

const updated = async (path) => {
  const p = await Deno.run({ cmd: ["git", "log", "-1", '--pretty="%cI"', "--", path], stdout: 'piped' })
  return new TextDecoder().decode(await p.output()).trim().replace(/"/g, '');
};

const pathToIds = (path) => {
  const parts = path.split('/');
  const key = parts.pop();
  const group = parts.pop()
  return {
    group: group,
    key: key.replace(/\.(csv|json)$/, ""),
  };
}

const makeMetadata = async (path) => {
  const { key, group } = pathToIds(path);
  const dateUpdated = await updated(path);
  const m = {
    key,
    group,
    path,
    updated: dateUpdated,
  }
  return m;
}

const grouper = (grouped, { group, key, ...info }) => {
  if (!grouped[group]) grouped[group] = {};
  grouped[group][key] = info;
  return grouped;
}
const metadata = await Promise.all(files.map(makeMetadata))

export default metadata.reduce(grouper, {});
