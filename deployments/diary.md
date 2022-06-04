# 23 Oct 2021

---

## Setup Google App Engine to host project

1. Create _fireside-games_ project in google cloud https://console.cloud.google.com/home/dashboard?project=fireside-games

2. Install development tools

   - google cloud sdk
   - google cloud sql proxy
   - terraform

3. Create project in GCP under 'no organization'

   - Replace _project_id_ in _terraform.tfvars_

4. Create 'Terraform' service account with 'Owner' role

   - Used by terraform to apply changes
   - Create JSON Key and append _.secret_ to the end of the name (for gitignore)
   - Place JSON Key in `deployments/terraform/<service account key>.json.secret`
   - Replace _terraform_service_account_key_ in _terraform.tfvars_

5. Configure Terraform variables

   - Set configurations in _terraform.tfvars_ such as regions

6. Run Terraform

   - Run _terraform plan_ and follow instructions to enable gcp services

   ```bash
   # in deployments/terraform

   terraform init
   terraform plan

   # follow instructions to enable gcp services
   ```

7. Prepare django project for App Engine deployment

   - Create _requirements.txt_
   - Create _main.py_
   - Create _app.yaml_
   - Create _.env_ (add to .gitignore and .gcloudignore - to be copied to secrets manager)
   - Create _.gcloudignore_ (ignore secrets and .env)

8. Store App Engine Service key in Secrets Manager

   - Create json key from default app engine service account
   - Base64 encode the json

     ```python
     from base64 import b64encode

     with open('path/to/key', 'rb') as f:
         content = f.read()
         print(b64encode(content).decode())
     ```

   - Copy the encoded string to the _APP_ENGINE_SVC_KEY_ variable in _.env_
   - Run _terraform plan + apply_ to create/update the secret

9. Set Cloud SQL database password

   - Go to GCP cloud console > SQL > choose instance > Users > Change Password
   - Copy password to _DB_PASSWORD_ variable in _.env_

10. Deploy to App Engine

    ```bash
    gcloud projects list
    gcloud config set project fireside-games
    gcloud app deploy
    ```

11. Perform initial migrations

    - Proxy database to local
      ```bash
      ./cloud_sql_proxy -instances=fireside-games:asia-southeast1:fireside-games-db=tcp:5432
      ```
    - Set _PROXY_DB=True_ in _.env.dev_
    - Migrate
      ```bash
      ./manage.py migrate
      ./manage.py createsuperuser
      ```

# 10 Oct 2021

---

## Initialize django project using django-soft-ui-dashboard

1. Copy over the following folders from _deps/django-soft-ui-dashboard_ to _firesideweb/_

   - apps/authentication (rename config.py to apps.py, modify accordingly)
   - apps/home (rename config.py to apps.py, modify accordingly)
   - static
   - templates
   - core/urls.py (fill in other apps as needed)

2. Add _home_ and _authentication_ to _settings/INSTALLED_APPS_

3. Fix all imports, paths, urls that reference _apps_
