# taricBookFinderBackend

Prueba Python Backend Junior para Taric S.A

Este backend fue codificado en Python, utilizando el framework Django.

Básicamente se encarga de publicar dos endpoints:

/books/[ISBN10, ISBN13 o ISBNdb ID]/

/books?q=[Query string]&index=[title, author, publisher o subject]&page=[número de página]

Los cuales se encargan de buscar y retornar los libros de ISBNdb.com y publicarlos para ser consumidos por el frontend.


## Añadir API Keys de ISBNdb en windows
```
> SET ISBN_API_KEY=[TU API KEY]
```

## Añadir API Keys de ISBNdb en linux
```
> export ISBN_API_KEY=[TU API KEY]
```

## Instalar paquetes requeridos
```
$ pip install -r requirements.txt
```

## Ejecutar pruebas
```
$ python manage.py test
```

## Ejecutar servidor django
```
$ python manage.py runserver 8001
```
