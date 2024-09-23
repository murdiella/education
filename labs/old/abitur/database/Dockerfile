FROM postgres
COPY postgresql.conf /etc/postgresql/postgresql.conf
RUN chown postgres /etc/postgresql/postgresql.conf
RUN chmod 600 /etc/postgresql/postgresql.conf
CMD ["-c", "config_file=/etc/postgresql/postgresql.conf"]
