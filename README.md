# Mindfulness-Voice

## Environments
check `requirements.txt`

## AWS Polly
To use the polly API, need to configure AWS authentication which is used in `app.py`
```python
# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="pollyuser")
```
For details about setting IAM user (with AWS CLI installed) check: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html#cli-configure-profiles-create

## Start the app

```shell
python -m flask run
```
Or run the `app.py` from your IDE
