import boto3
import click


def identity_arn(region):
    sts_client = boto3.client('sts', region_name=region)

    response = sts_client.get_caller_identity()

    return {
        'User ID': response.get('UserId'),
        'ARN': response.get('Arn')
    }


@click.command()
@click.option('--profile', default='default', help='AWS CLI profile name')
@click.option('--region', default='cn-north-1', help='AWS region')
def role_token(profile, region):
    session = boto3.Session(profile_name=profile)
    credentials = session.get_credentials()

    credential = {
        'access_key': credentials.access_key,
        'secret_key': credentials.secret_key,
        'token': credentials.token
    }

    print(identity_arn(region))
    print(credential)


if __name__ == "__main__":
    role_token()
