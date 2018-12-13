.PHONY: all prepare-env create_manual create_db build uninstall run_pokemon_client run_pokemon_server

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
	@echo $(UNAME_S)
	@if [ $(UNAME_S) = "Darwin" ]; then \
		cp manpages/pokemon_server.1 /usr/local/share/man/man1/pokemon_server.1; \
		gzip /usr/local/share/man/man1/pokemon_server.1; \
		cp manpages/pokemon_client.1 /usr/local/share/man/man1/pokemon_client.1; \
		gzip /usr/local/share/man/man1/pokemon_client.1; \
		echo OK; \
	else \
		cp manpages/pokemon_server.1 /usr/local/man/man8/pokemon_server.1; \
		gzip /usr/local/man/man8/pokemon_server.1 \
		cp manpages/pokemon_client.1 /usr/local/man/man8/pokemon_client.1; \
		gzip /usr/local/man/man8/pokemon_client.1 \
		echo OK; \
	fi

create_db:
	@mkdir DB

build: create_manual create_db
	@echo OK

clean:
	@rm -rf DB

run_pokemon_client:
	@python3 client.py

run_pokemon_server:
	@python3 server.py
