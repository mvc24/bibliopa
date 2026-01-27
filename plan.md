# What I need to create a working platform

## Backend
- Queries
- Authentication, users & sessions, cookies
- create new entries
- edit entries
- Search functionality
- Download search results, sections, entire bibliography as pdf/csv

### Roles/Permissions

- admin: just me, can do everything
- family/special: prices are displayed, can add/edit/delete entries, add prices to an entry, download documents
- user/guest: can download results, no prices displayed
- no login: can browse/search bibliography, no prices displayed, no downloads
  
## Frontend

### Pages

- Login
- Landing
- Bibliography
- Project description/overview to showcaase technical aspects (because this is a portfolio project to become a data engineer)
- Impressum/Contact

### Input/Forms

- Create account (only guest/standard account; special/family can only be created by me directly)
- Create new entry
- Edit existing entry
- Remove a book from collection (happens quite regularly, should be easy)
- Add a new price to an entry with source (this is a new functionality that wasn't there before: my grandfather researches prices from different online antiquariat booksellers and can add the prices he sees with the link, date is added automatically. This way a price development can be tracked.)
- Edit person information stored in people table (e.g. if the "authority record" isn't correct)
- Troubleshooting from my grandpa to me:
  - A book should exist but can't be found (might be part of data that still needs extra processing, but isn't in the database yet)
  - A person seems to exists twice
  - Easy way to create a "bug report", if possible with detailed error logging for me that he doesn't need to understand

## UX and other thoughts

- Accessibility is very important. The main end user is nearly 90 years old. He has a bit of a tremor in his hands, so buttons and fields need to be easy to navigate
- I need a way for my grandfather to easily flag something for me to review or to report bugs, like a simple "send to M." button or form with a few checkboxes for common issues 
- When adding a new entry, as much data as possible should be suggested or available as checkbox/radio, e.g. publisher, place, condition, ... The people information needs to be cross-checked before creating a new record (i.e. does this person already exist in my people table, if yes, use that)
