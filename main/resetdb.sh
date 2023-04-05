#!/bin/sh
docker exec -it paycash_db psql -U postgres postgres -c 'REVOKE ALL PRIVILEGES ON DATABASE "paycash" FROM paycash_user;' -c "REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM paycash_user;" -c 'DROP DATABASE "paycash";'  -c "DROP USER paycash_user;"
docker exec -it paycash_db psql -U postgres postgres -c "CREATE USER paycash_user WITH PASSWORD 'paycash';" -c 'CREATE DATABASE "paycash" OWNER paycash_user;' -c 'GRANT ALL PRIVILEGES ON DATABASE "paycash" TO paycash_user;' -c 'GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "paycash_user";'
