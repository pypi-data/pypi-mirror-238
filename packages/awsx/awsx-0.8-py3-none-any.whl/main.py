import boto3
import click


def identity_arn(region):
    sts_client = boto3.client('sts', region_name=region)

    # 使用 get_caller_identity 获取调用者的身份信息
    response = sts_client.get_caller_identity()

    return {
        'User ID': response.get('UserId'),
        'ARN': response.get('Arn')
    }


@click.command()
@click.option('--profile', default=None, help='AWS CLI profile name')
@click.option('--region', default='cn-north-1', help='AWS region')
def role_token(profile, region):
    if profile:
        session = boto3.Session(profile_name=profile)
    else:
        session = boto3.Session()

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
