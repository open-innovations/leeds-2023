# leeds-2023


## Website Development

The public-facing website is located in the `docs` folder.

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

###Using on Windows Local Machine

1. Download and install ruby 2.7.3 from https://rubyinstaller.org/downloads/archives/
2. Install jekyll - `gem install jekyll`
3. Run `bundle install` 
4. Add the line `require 'em/pure_ruby'` to very top of this file 
Ruby27-x64\lib\ruby\gems\2.7.0\gems\eventmachine-1.2.7-x64-mingw32\lib\eventmachine.rb
5. bundle exec jekyll serve --baseurl /leeds-2023 --livereload --open-url