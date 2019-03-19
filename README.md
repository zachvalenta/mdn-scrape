# what is this?

POC that uses:

* __Scrapy__ 🕸🕷🕸 for a quick and dirty scrape of an MDN subdomain
* __Algolia__ 🏎🔍🏎 for typeahead search

# how to run?

short answer: `make help` 🙂

long answer: ⤵️

* __UI__: all you'll need is a browser, just use `make search` (swap in `xdg-open` if you're running Linux)
* __backend__: you'll need...
    - Python 3.4+
    - virtual environment: create it in the project root, activate, and then run `make pipin` to pull down the dependencies
    - `.env`: create it in the project root, then add Algolia API keys (`APP_ID`, `API_KEY_ADMIN`)
