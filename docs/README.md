# leeds-2023 Data Microsite

### Preparation

Change directory into the `docs` folder.

1. Have a working Ruby [installation](https://www.ruby-lang.org/en/documentation/installation/).
   There are many, many approaches to this.
   The Windows Subsystem for Linux might be worth looking into.
   Version 2.7.3 is the version used by Github Pages at present.
   It might be worth considering installing `rbenv` to manage versions.
2. Install bundler - `gem install bundler`.
3. Run `bundle install`.

### Serving the site locally

From within the `docs` folder.

```bash
bundle exec jekyll serve --baseurl /leeds-2023 --livereload --open-url
```

### Serving the site locally on a Windows Local Machine (Ruby Installer for Windows)

1. Download and install Ruby+Devkit 2.7.3 from https://rubyinstaller.org/downloads/archives/

2. Change directory into the `docs` folder and run `bundle install` 
3. Reinstall eventmachine `gem uninstall eventmachine`	`gem install eventmachine --platform=ruby`

4. From within the `docs` folder...

```bash
bundle exec jekyll serve --baseurl /leeds-2023 --livereload --open-url
```