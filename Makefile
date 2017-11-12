.PHONY: test
test:
	py.test --doctest-modules server

.PHONY: run
run:
	python server.py

.PHONY: start_postgres
start_postgres:
	pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start