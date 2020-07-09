#!/bin/bash
_now=$(date +"%Y%m%d%H%M%S")
_file="backup/backup_$_now.sql"
docker exec krabshack_project_postgres_1 pg_dump -U postgres -d postgres > "$_file"
