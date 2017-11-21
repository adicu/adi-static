# ADI Website

[![Build Status](https://travis-ci.org/adicu/adi-static.svg?branch=master)](https://travis-ci.org/adicu/adi-static)

ADI is the tech club at Columbia. This is the source code for our website,
built with [Lektor](http://getlektor.com/)!

## Setup

1. Install [Lektor](http://getlektor.com/)
2. Install npm
3. Run `lektor server -f webpack` and go visit `localhost:5000/admin`!

## Under the Hood

### Deployment

Right now, we mostly rely on Travis-CI to deploy after each successful
build. If you want to deploy manually and have the permissions on our
server, you should be able to run `lektor deploy production`.

### Scraping Facebook

Because of Facebook's deliberately crippled API, we actually update our
website based on Facebook events instead of the other way around. Right
now, we use Travis's nightly cron to run `./scripts/travis-commit.sh`,
wich should do the rest.

## Code Organization

```
.
├── .travis.yml
├── adi-static.lektorproject    -- Lektor project configuration
├── assets
│   └── static
│       ├── css
│       ├── gen                 -- Assets that are generated via webpack
│       └── img
├── content                     -- Vanilla Lektor content
├── databags
│   └── meta.ini                -- Some basic metadata
├── flowblocks                  -- Lektor flowblocks (see also templates/blocks)
├── models                      -- Defines Lektor's data schema
├── packages
│   └── events
│       ├── lektor_events.py    -- Some magic to get future and past events
│       └── setup.py
├── README.md
├── scripts
│   ├── get_facebook_events.py  -- Scrapes FB and updates content/
│   ├── install.py
│   └── travis-commit.sh
├── templates                   -- Lektor templates (in Jinja2)
└── webpack
    ├── js
    ├── package.json
    ├── scss                    -- Where most of the styling lives
    └── webpack.config.js

```
