/**
 * auto-dependency
 * 
 * Usage:
 * 
 *   import autoDependency from '<this file>'
 *   site.process(['.html'], autoDependency)
 * 
 * This will search a built dom tree for data-dependencies attributes and add a script element for each.
 * 
 */
export default function (page: any) {
  // Search for all elements on page with a data-dependencies attribute and turn into an Array
  const elementsWithDepenencies = Array.from(
    page.document.querySelectorAll('[data-dependencies]')
  );
  // If none found, finish processing
  if (elementsWithDepenencies.length === 0) return;

  // For each element in the list,
  // get data-dependencies attribute,
  //   split the string each list (to allow for multiple dependencies)
  //   and trim whitespace
  // then flatten the list (un-nest lists)
  const fullDependencyList = elementsWithDepenencies
    .map((element: any) =>
      element
        .getAttribute('data-dependencies')
        .split(',')
        .map((dependency: string) => dependency.trim())
    )
    .flat();

  // Finally deduplicate by creating a Set, then converting to an Array.
  // A Set has the property that values are stored only once.
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set
  const deduplicatedDependencies = Array.from(new Set(fullDependencyList));

  // For each deduplicated depdency
  deduplicatedDependencies.forEach(dependency => {
    // Create a new script element
    const newScriptElement = page.document.createElement('script');
    // Set the src attribute
    newScriptElement.setAttribute('src', dependency);
    // And set a data-auto-depdendency attribute
    newScriptElement.setAttribute('data-auto-dependency', true);
    // Then append to the document head
    page.document.head.appendChild(newScriptElement);
  });
}
