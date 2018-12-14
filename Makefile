.PHONY: all prepare-env create_manual create_db build run_pokemon_client run_pokemon_server

UNAME_S=$(shell uname -s)

all:
	@echo "make prepare-env"
	@echo "    Prepara el entorno."
	@echo "    Se necesita ejecutar con sudo para instalar el manejador de paquetes de Python3."
	@echo "make create_manual"
	@echo "    Crea los manuales del proyecto."
	@echo "make create_db"
	@echo "    Crea el directorio de la base de datos."
	@echo "make build"
	@echo "    Creates debian package."
	@echo "make clean"
	@echo "    Limpia el proyecto y eleimina los archivos generados en el build."
	@echo "make run_pokemon_client"
	@echo "    Ejecuta el cliente de Pokemon."
	@echo "make run_pokemon_server"
	@echo "    Ejecuta el servidor de Pokemon."

prepare-env:
	@if [ $(UNAME_S) = "Darwin" ]; then \
		easy_install pip; \
		echo OK; \
	else \
		apt-get install python3-pip; \
		echo OK; \
	fi
	@pip3 install -r requirements.txt

create_manual:
	@if [ $(UNAME_S) = "Darwin" ]; then \
		cp manpages/pokemon_server.1 /usr/local/share/man/man1/pokemon_server.1; \
		gzip /usr/local/share/man/man1/pokemon_server.1; \
		cp manpages/pokemon_client.1 /usr/local/share/man/man1/pokemon_client.1; \
		gzip /usr/local/share/man/man1/pokemon_client.1; \
		echo OK; \
	fi

create_db:
	@if [ ! -d "src/DB" ]; then \
		cd src && mkdir DB && python3 init_db.py; \
		echo "La base de datos fue inicializada"; \
	fi
	@echo OK;

build: create_manual create_db
	@echo OK

manual_pokemon_server:
	@man ./manpages/pokemon_server.1

manual_pokemon_client:
	@man ./manpages/pokemon_client.1

clean:
	@rm -rf src/DB 2> /dev/null || true
	@rm -rf src/__pycache__ 2> /dev/null || true
	@rm src/*.png 2> /dev/null || true

run_pokemon_client:
	@cd src && python3 client.py

run_pokemon_server:
	@cd src && python3 server.py
