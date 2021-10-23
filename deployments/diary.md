
# 23 Oct 2021
--------------------------------------------------------------------------------------------

## Setup Google App Engine to host project

1. Create *fireside-games* project in google cloud https://console.cloud.google.com/home/dashboard?project=fireside-games

2. Install development tools
    - google cloud sdk
    - google cloud sql proxy
    - terraform

3. Create project in GCP under 'no organization'
    - Replace *project_id* in *terraform.tfvars*

4. Create 'Terraform' service account with 'Owner' role
    - Used by terraform to apply changes
    - Create JSON Key and append *.secret* to the end of the name (for gitignore)
    - Place JSON Key in `deployments/terraform/<service account key>.json.secret`
    - Replace *terraform_service_account_key* in *terraform.tfvars*

5. Configure Terraform variables
    - Set configurations in *terraform.tfvars* such as regions

6. Run Terraform

    - Run *terraform plan* and follow instructions to enable gcp services

    ```bash
    # in deployments/terraform

    terraform init
    terraform plan

    # follow instructions to enable gcp services
    ```

7. Prepare django project for App Engine deployment

    - Create *requirements.txt*
    - Create *main.py*
    - Create *app.yaml*
    - Create *.env* (add to .gitignore and .gcloudignore - to be copied to secrets manager)
    - Create *.gcloudignore* (ignore secrets and .env)

8. Store App Engine Service key in Secrets Manager

    - Create json key from default app engine service account
    - Base64 encode the json
        ```python
        from base64 import b64encode

        with open('path/to/key', 'rb') as f:
            content = f.read()
            print(b64encode(content).decode())
        ```
    - Copy the encoded string to the *APP_ENGINE_SVC_KEY* variable in *.env*
    - Run *terraform plan + apply* to create/update the secret

9. Set Cloud SQL database password

    - Go to GCP cloud console > SQL > choose instance > Users > Change Password
    - Copy password to *DB_PASSWORD* variable in *.env*

10. Deploy to App Engine

    ```bash
    gcloud projects list
    gcloud config set project fireside-games
    gcloud app deploy
    ```

# 10 Oct 2021
--------------------------------------------------------------------------------------------

## Initialize django project using django-soft-ui-dashboard

1. Copy over the following folders from *deps/django-soft-ui-dashboard* to *firesideweb/*

    - apps/authentication (rename config.py to apps.py, modify accordingly)
    - apps/home (rename config.py to apps.py, modify accordingly)
    - static
    - templates
    - core/urls.py (fill in other apps as needed)

2. Add *home* and *authentication* to *settings/INSTALLED_APPS*

3. Fix all imports, paths, urls that reference *apps*
