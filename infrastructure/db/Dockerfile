FROM postgres:16-alpine

# Bake init.sql into the image so ECS doesn't need volume mounts
COPY init.sql /docker-entrypoint-initdb.d/init.sql
