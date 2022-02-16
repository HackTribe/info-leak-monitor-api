# info-leak-monitor-api
Git information leakage monitoring

# Usage
See Developer API docs (http://127.0.0.1/api/docs).

# Deployments
## Configure
before using, you need to set the MySQL user name and address. To use the data migration tool, you need to set the `alembic.ini` configuration file.
You can use environment variables or `.env` configuration file. For more information, refer to the `app.core.config` Python configuration file

## Source Deploy
```shell
git clone https://github.com/HackTribe/info-leak-monitor-api.git && cd info-leak-monitor-api && sudo docker-compose up -d
```

## Deploy
using `docker-compose` deploy.
```
docker-compose -f docker-compose.yaml up -d
```
import database table structure.
```
mysql -u root -p info-leak-monitor < init-db.sql
```
or use alembic tools initialization database.
```
docker exec -it info-leak-monitor-api /bin/bash
#> alembic revision --autogenerate -m "init" && alembic upgrade head
```

## Admin
use `init-db.sql` file initialization database.
- user `admin`
- password `meiyoumima`

if you use alembic tools initialization database. need using `API` add users. see API docs (http://127.0.0.1/api/docs).

## Dependencies
- Docker
- Docker Compose

# FAQ

# Donate
if you think the it's helpful for you, please consider paying a cup of coffee for me. Thank you!
