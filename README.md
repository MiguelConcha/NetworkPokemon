# Proyecto de Redes de Computadoras

:computer: :envelope: :left_right_arrow: :left_right_arrow: :left_right_arrow: :envelope: :computer:

<img width="572" alt="screen shot 2018-12-16 at 10 32 38 am" src="https://user-images.githubusercontent.com/13952922/50056163-fc4b8d80-011d-11e9-8909-dd9ecff385ff.png">

* Profesor: Paulo Santiago de Jesús Contreras Flores.
* Ayudante: Virgilio Castro Rendón.
* Laboratorio: José Daniel Campuzano Barajas.

Redes de computadoras - Facultad de Ciencias, UNAM.

## Descripción del proyecto

Se programó un protocolo para la capa de aplicación que consiste en que un cliente solicita al servidor iniciar el juego de capturar un _Pokémon_. Luego de haber iniciado sesión:
 * El cliente solicita jugar y el servidor le ofrece aleatoriamente un _pokémon_ a capturar. 
 * El cliente responde si desea o no proceder a intentar capturar al _pokémon_ en cuestión.
 * El servidor captura o no al _pokémon_ aleatoriamente y pregunta al cliente en caso de fallo si desea intentarlo nuevamente, decrementando un contador de oportunidades que inicializó antes aleatoriamente en un rango determinado.
 * En caso de haberlo capturado, el cliente recibe una imagen del _pokémon_ que es guardada en el equipo.
 * Se termina la sesión y se cierra la conexión.
 
Para la implementación se usó un esquema previamente definido de mensajes y un Autómata Finito Determinista de estados (AFD, _FSM_, _Finite State Machine_). Se pretende _vender_ el protocolo.

## Entorno

* **`OS`**: macOS Mojave o Ubuntu 18
* **`Python`**: Python 3.7.0
* **`pip3`**: pip 18.0

# Ejecución del programa

Para mostrar lo que puede hacer el archivo `Makefile` se deberá ejecutar el 
siguiente comando. Ésto servirá de ayuda ya que dice que hace en cada fase.
```bash
make
```

Para poder ejecutar el cliente y el servidor se utilizó un paquete de Python que
debe ser instalado, para ello, se debe instalar `pip3` e instalar un paquete.
Para hacer todo esto basta con ejectura lo siguiente con `sudo`.
```bash
make prepare-env
```

Una vez ya preparado el ambiente con `make prepare-env` se procederá a instalar
la aplicación y el manual de Unix de éste.
```bash
make build
```

Si se quiere limpiar el proyecto se deberá ejecutar el siguiente comnado.
```bash
make clean
```

---

Para ejecutar el cliente o el servidor, se necesita haber ejecutado previamente
`make prepare-env` seguido de `make build`.

Si se desea correr el cliente se deberá ejecutar el siguiente comando
```bash
make run_pokemon_client
```

Si se desea correr el servidor se deberá ejecutar el siguiente comando
```bash
make run_pokemon_server
```

# Manuales de Unix

Si se ejecuta en entorno Mac se podrá ver los manuales de la siguiente manera 
después de haber ejecutado `make build`.
```
man pokemon_client
```

```
man pokemon_server
```

Encontramos un inconveniente y en diferentes versiones de Linux se ponen en 
los manuales de Unix en diferentes ubicaciones, para no lidiar con esto, 
no se instalarán los manuales, pero se podrán visualizar con los siguientes 
comandos.
```
make manual_pokemon_server
```

```
make manual_pokemon_client
```

---

Se creo dos PDFs de los manuales de Unix en en directorio `manpages`.

# Reporte

En el [reporte](reporte.pdf) se describen los aspectos técnicos de la implementación del protocolo, así como la tabla que detalla los estados y mensajes transmitidos, el FSM y también el documento para la venta de la aplicación; se incluye un apartado que incluye la evidencia con las capturas del tráfico en _Wireshark_.

## Documentación

La documentación fue hecha con la herramienta 
[Sphinx](http://www.sphinx-doc.org/en/1.5/index.html#). Se generó un html con toda la documentación en el directorio `doc` dentro de éste solo se debe abrir el archivo llamado `index.html`.


## Integrantes

* Andrés Flores Martínez - *(`andresfm97@ciencias.unam.mx`)*
* Ángel Iván Gladín García - *(`angelgladin@ciencias.unam.mx`)*
* Miguel Concha Vázquez  - *(`mconcha@ciencias.unam.mx`)*
