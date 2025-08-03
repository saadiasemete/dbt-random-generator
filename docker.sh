docker run --name test-postgres \
  -e POSTGRES_USER=dbt_user \
  -e POSTGRES_PASSWORD=dbt_pass \
  -e POSTGRES_DB=dbt_db \
  -p 5432:5432 \
  -d postgres:15