# keycloak fdw

if you're not seeing changes after `make install` then make sure pip is using --upgrade and the version is what you expect. if you have postgres installed with python3 support the makefile should be using pip3, otherwise pip2, etc.

If you see an ImportError when trying to `CREATE SERVER` doublecheck your python versions and make sure you're running setup.py with the version Postgres expects.

# first time setup

```bash
$ sudo easy_install pgxnclient
$ sudo pgxn install multicorn
$ psql assure -c 'create extension multicorn;'
```

# build fdw

some of this may be redundant

```bash
$ make && make install
$ sudo python setup.py install
$ brew services restart postgresql
```

### Troubleshooting
#### On mac...
edit Makefile (line 93), change darwin to Darwin
make
sudo ARCHFLAGS="-arch x86_64" make install
