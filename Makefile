.PHONY: tests shell clean

TESTS_SERVICE=tests

shell:
	docker-compose run --rm ${TESTS_SERVICE} sh -c '/bin/sh'

tests:
	docker-compose run --rm ${TESTS_SERVICE} sh -c 'mamba tests -f documentation'

clean:
	docker-compose stop; docker-compose rm -f
