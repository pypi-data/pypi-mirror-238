## Features

Some of it’s stand out features are:

- Koppeltaal 2.0 SDK
- FHIR Koppeltaal 2.0 profiles validation
- JWKS utils
- `kt` commandline application

## Developer Guide

This guide gives a brief overview of the core Koppeltaal 2.0 concepts and how to integrate with its services

### Important differences with Koppeltaal 1.x

| Concept            | KT 1.x                                      | KT 2.0                       |
| ------------------ | ------------------------------------------- | ---------------------------- |
| FHIR Exchange      | Messaging                                   | RESTful API                  |
| Content Validation | Separate service                            | Built-in                     |
| Authorisation      | None - application has access to everything | On resource &amp; CRUD-level |

#### FHIR Exchange

By using the (FHIR) RESTful API exchange there is a single source of truth. Koppeltaal 1.x acted as a message broker, giving each participant the responsibility to keep all data up-to-date.
Another big advantage is that Koppeltaal 2.0 works with small messages. So no self-contained bundles. This saves a lot of data being transferred over the line and the chance of 409 Conflicts are considerably reduced.

#### Content Validation

Previously, a separate service could be used to check whether the content of a Bundle is valid. However, this validation was not enforced by the Koppeltaal server.
Koppeltaal 2.0 uses profiles. A profile indicates exactly what the rules are per Resource. The Koppeltaal server can enforce profiles by validating that the Resources adhere to the profile.

#### Authorisation

Applications connect to the Koppeltaal server. Within "Domeinbeheer" (Domain Management), roles are assigned to the applications. A role can contain multiple CRUD permissions per Resource. With Koppeltaal 2.0, you are only allowed to work with resources to which you are entitled. With Koppeltaal 1.x, applications can see everything that they are subscribed to within a Domain.

## Usage

### Configuration

Create a `koppeltaal.toml` file with the neccessary configuration:

```toml

client_name = "name-of-customer-or-client"
fhir_url = "https://foo.koppeltaal.nl/api/v1/healthcareinc/fhir/r4/"
oauth_token_url = "https://foo.koppeltaal.nl/api/v1/healthcareinc/oauth2/token"
oauth_authorize_url = "https://foo.koppeltaal.nl/api/v1/healthcareinc/oauth2/authorize"
oauth_introspection_token_url = "https://foo.koppeltaal.nl/api/v1/healthcareinc/oauth2/token/introspection"
smart_config_url = "https://foo.koppeltaal.nl/api/v1/healthcareinc/fhir/r4/.well-known/smart-configuration"
domain = "https://foo.koppeltaal.nl"
client_id = "uuid-client-id"


```

### Commandline interface

`kt help`

```
Usage: kt [OPTIONS] COMMAND [ARGS]...

  Koppeltaal command line tool

Options:
  --debug        enable debug logs ( default: False )
  --config TEXT  select config file
  --help         Show this message and exit.

Commands:
  activitydefinition   get single activitydefinition resource by id from
                       koppeltaal api
  activitydefinitions  get all activitydefinition resources from koppeltaal
                       api
  endpoint             get single endpoint resource by id from koppeltaal api
  endpoints            get all endpoint resources from koppeltaal api
  info                 show Koppeltaal api info
  patient              get single patient resource by id from koppeltaal api
  patients             get all patient resources from koppeltaal api
  practitioner         get single practitioner resource by id from koppeltaal
                       api
  practitioners        get all practitioner resources from koppeltaal api
  task                 get single task resource by id from koppeltaal api
  tasks                get all task resources from koppeltaal api
  version              show Koppeltaal cli version
```

### Python Shell

```shell
make shell
```

## Documentation

## Roadmap

-

## Is it any good?

[Yes.](http://news.ycombinator.com/item?id=3067434)

## License

The MIT License

## Credits

Part of this document is released under the Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) license.
