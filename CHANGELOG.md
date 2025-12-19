# Changelog

## 0.3.0
### Added
- Experimental diet code parsing on Compass-group parser. This one handle diet
code parsing with regex and dictionary, which is a bit better at handling 
diet codes that are embedded in food strings.
- Parser for Unicafe. Due to how Unicafe dates is delivered, I also added
  locales library to handle different day name format.
- Menu group information is now available. With this addition, you can see each menu group much more clearly.
- Logger to improve debugging.

### Updates
- Changed database insert strategy: Instead of dropping all tables altogether on every new transaction, add only new data and keep the old one. This is a step towards implementing db update on existing menu if a change was detected and deleting data older than a certain amount of time.
- Fixed db_check not running in sync with Finnish timezone.
- Group all Flask-related files and utils to src/app/.
- Fixed variables in context_processor not passed into Jinja2 templates
- Changed restaurant name font to Playpen Sans.
- Various UI changes aimed to improve readability and structure.
- Compass-group parser: Improved menu string handling and menu parsing when
restaurant is not open.
- Sodexo parser: Improved parsing menu when restaurant is not open.

### Misc
- Removed the deprecated (in Python 3.9) typing.List and use built-in list
  instead.
- Refactoring various modules.
- Improved documentations.

## 0.2.0
### Added
- Filter restaurants based on area in a city.
- Parser for TAMK Campusravita.

### Updates
- Minor fixes and code cleanup.
- Restructured Juvenes parser: now can recognize essential chunk from the JSON response based on restaurant's ID and menuTypeID, and only process those instead of the whole response.

## 0.1.0
Initial release.

