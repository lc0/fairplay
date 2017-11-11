.PHONY: test
test:
	py.test --doctest-modules server

.PHONY: run
run:
	python server.py