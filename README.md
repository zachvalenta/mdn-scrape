# what is this?

POC that uses:

* __Scrapy__ 🕸🕷🕸 for a a quick and dirty scrape of an MDN subdomain
* __Algolia__ 🏎🔍🏎 for typeahead search

# how to run?

shorter answer: `make help` 🙂

longer answer

* __UI__: all you'll need is a browser, just use `make search` (swap in `xdg-open` if you're running Linux)
* __backend__: you'll need 
    - Python 3.4+
    - dependencies: make a virtual environment, activate it, then run `make pipin`
    - an `.env` file in the project root with API keys for Algolia, specifically `APP_ID` and `API_KEY_ADMIN`
