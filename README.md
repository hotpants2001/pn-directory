# Coach Directory - PN Assignment Jon
*Implemented in Python/Django.*

Exercise #1 - Build a Certified Coach Directory API

When a coach completes one of the PN certification programs they need to have their credentials displayed on a webapp. 

The directory will be searchable by Country, Postal Code and Name.

Each entry will display:

Name, Certification Level, Tagline, Business Name, Location, Mobile, Website, Email

Note that the provided database does not have the exact same fields, it’s up to you to decide how to expose the ones that are “computed” (i.e. address)
“Certification Level” can be calculated based on “level_1” and “level_2” 

## Deploy to Heroku
```shell
$ heroku create -a pn-directory
$ heroku container:push -a pn-directory web && heroku container:release -a pn-directory web
```

## Tests

```shell
$ ./manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....................
----------------------------------------------------------------------
Ran 20 tests in 0.085s

OK
Destroying test database for alias 'default'...
```
