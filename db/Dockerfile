FROM postgres
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB pump
COPY db/schema.sql /docker-entrypoint-initdb.d/
