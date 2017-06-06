from setuptools import setup

setup(name     = "keycloak",
  version      = "1.0.0",
  description  = "PostgreSQL foreign data wrapper for keycloak's REST api",
  author       = "Harris Schneiderman",
  author_email = "harris.schneiderman@deque.com",
  packages     = ["keycloak"],
  install_requires=["requests"]
)
