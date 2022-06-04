# Local Development

## To connect to production database

- Run cloud proxy

  ```bash
  ./cloud_sql_proxy -instances=fireside-games:asia-southeast1:fireside-games-db=tcp:5432
  ```

- Set _PROXY_DB=True_ in _.env.dev_
