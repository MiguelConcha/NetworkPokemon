# Proyecto de Redes de Computadores

Maik aquí ponle cosas. :squirrel:

Redes de computadoras - Facultad de Ciencias, UNAM.

## Descripción del proyecto

Maik aquí ponle cosas. :squirrel:


## Entorno

* **`OS`**: macOS Mojave o Ubuntu 18
* **`Python`**: Python 3.7.0
* **`pip3`**: pip 18.0

# Ejecucicón del programa

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

Para ejecutar el cliente o el servidor, se abrá necesitado ejecutar previamente
`make prepare-env` seguido de `make build`.

Si se desea correr el cliente se deberá ejecutar el siguiente comnado
```bash
make run_pokemon_client
```

Si se desea correr el servidor se deberá ejecutar el siguiente comnado
```bash
make run_pokemon_server
```

# Manueles de Unix

Una vez ejecutado el comando `make build` se habrá creado dos manuales, uno del 
servidor y otro del cliente.

Para acceder a ellos basta con ejecutar los siguientes comandos respectivamente.

```
man pokemon_client
```

```
man pokemon_server
```

# Captura del tráfico de Wireshark

Maik aquí ponle cosas. :squirrel:

# Reporte

Maik aquí ponle una liga al documento de latex.

## Documentación

La documentación fue hecha con la herramienta 
[Sphinx](http://www.sphinx-doc.org/en/1.5/index.html#). Se generó un html con toda la documentación en el directorio `doc` dentro de éste solo se debe abrir el archivo llamado `index.html`.


## Integrentes

* Andrés Flores Martínez - *(`andresfm97@ciencias.unam.mx`)*
* Ángel Iván Gladín García - *(`angelgladin@ciencias.unam.mx`)*
* Miguel Concha Vázquez  - *(`javierem_94@ciencias.unam.mx`)*
