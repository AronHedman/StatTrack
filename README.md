# Docker-compose LEMP
## Inkluderar
- nginx 
- SvelteKit -> localhost
- php -> /api/
- mariadb -> mariadb
- phpmyadmin -> localhost:8080

## HowTo
### Node version
Se till att du har minst version 18.13 av nodejs.    
Kontrollera i terminalen med 
```sh
node -v
```

### SvelteKit
SvelteKit-projekt skapas i katalogen **sveltekit**
```sh
cd sveltekit
npx sv create
npm i
```
### API med php
Backend skrivet i php skall ligga i

    /www/public/api
### Starta servern (containern) med
    docker compose up -d
### Stoppa servern (containern) med
    docker compose down

### Logga SvelteKit till terminalen
Tyvärr loggas inte fel från Sveltekit till terminlalen.
Öppna en ny terminal och skriv:

````console
docker logs -f <Namnet på node-containern>
````
### Serverns url
    localhost
### phpmyadmin
    localhost:8080
### Anslut till MariaDB med php

````php
<?php
    // Definierar konstanter med användarinformation.
    define ('DB_USER', 'userName'); // Användare i MariaDB
    define ('DB_PASSWORD', '12345');
    define ('DB_HOST', 'mariadb');
    define ('DB_NAME', 'dbName');   // Databasen som anslutning skall ske till

    // Skapar en anslutning till MariaDB och databasen dbName
    $dsn = 'mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8';
    $db = new PDO($dsn, DB_USER, DB_PASSWORD);
?> // Ej nödvändigt att avslut "ren" php med ?>
````
### ToDo
    Stöd för https, TLS (ssl).
