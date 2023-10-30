
# Changelog
All notable changes to Messkit will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.1.8] - 2023-10-29
### Changed
- Remove custom emails collection.

## [0.1.7] - 2023-02-03
### Changed
- Remove custom list of app settings.
- Add default settings for class/table prefix.
- Use parent methods for print/prompt in install command.
- Use upstream logic for install command, and some web menus.

## [0.1.6] - 2022-12-28
### Changed
- Expose some more app settings.
- Add ASGI app wrapper.

## [0.1.5] - 2022-03-07
### Changed
- Keep `docs/_static/` folder around to prevent doc build errors.
- Force master doc to 'index' for Sphinx.
- Restrict which email settings come out of the box.
- Add `enum` module, include whatever poser says.

## [0.1.4] - 2022-03-05
### Changed
- Remove `--reload` flag from suggested web app command.

## [0.1.3] - 2022-03-05
### Changed
- Nod to mysql in the installer intro msg.
- Add `web/static/img` folder to manifest.

## [0.1.2] - 2022-03-05
### Changed
- Set default theme and images when installing.
- Include app setting for production flag.
- Add support for including some views based on DB settings.
- Add support for mysql database as messkit backend.
- Add upgrade script/config to installer.
- Add initial docs.

## [0.1.1] - 2022-03-03
### Added
- Initial version...sort of.
