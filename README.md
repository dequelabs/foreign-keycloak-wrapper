# Keycloak Single Sign-On Foreign Data Wrapper

[Keycloak](https://www.keycloak.org) is an open-source single sign-on and identity management provider. This foreign data wrapper allows PostgreSQL databases to federate Keycloak realms as foreign tables in order to query user information alongside application data.

Use of materialized views to cache users in Postgres is recommended since the Keycloak API call can add query time, especially if user data is being joined to other queries.

# Installation

## Prerequisites

PostgreSQL must be linked against Python in order to use Multicorn extensions. You can check whether Python is enabled by examining the output of `pg_config --configure` for the `--with-python` flag.

Multicorn must be installed alongside foreign-keycloak-wrapper. This is available through PGXN or can be installed manually. On OSX there may be issues which necessitate a manual install; see Troubleshooting below.

After installing foreign-keycloak-wrapper, PostgreSQL must be restarted.

## Python Versions

Whether Postgres uses Python 2 or 3 is important: this determines the appropriate installation directory for the extension. `pg_config --configure` may show a `PYTHON` environment variable, or your package manager may show which version of Python Postgres was built with (`brew info postgresql`). Unfortunately, there is not a consistent way to determine the correct version.

If Postgres' Python version is different from your system Python (`python --version`) you will need to set the `PYTHON` environment variable to the correct Python executable when installing.

## PGXN

To use PGXN, install `pgxnclient` through `pip`.

PostgreSQL

```bash
$ pgxn install foreign-keycloak-wrapper
```

## Manually

Install Multicorn, then clone this repository.

```bash
$ make install
```

# Usage

```sql
CREATE EXTENSION IF NOT EXISTS multicorn;

DROP SERVER IF EXISTS keycloak_users CASCADE;

CREATE SERVER keycloak_users FOREIGN DATA WRAPPER multicorn OPTIONS(
  wrapper 'keycloak.Keycloak',
  url 'url-of-keycloak-server',
  username 'admin-username',
  password 'admin-password',
  client_id 'name-of-confidential-keycloak-client',
  grant_type 'password',
  client_secret 'confidential-keycloak-client-secret'
);

CREATE FOREIGN TABLE realm_users (id uuid, username text, "firstName" text, "lastName" text, email text) SERVER keycloak_users;

SELECT * FROM realm_users;
```

If you see an ImportError when trying to `CREATE SERVER` doublecheck your python versions and make sure foreign-keycloak-wrapper is installed to the site-packages directory of the Python version Postgres expects.

# Troubleshooting

## Multicorn on OSX

In [some OSX environments](https://github.com/Kozea/Multicorn/issues/139) Multicorn must be installed manually. Clone the [Multicorn repository](https://github.com/Kozea/Multicorn) and edit the Makefile, changing `darwin` to `Darwin`. Then `make && sudo ARCHFLAGS="-arch x86_64" make install`.
