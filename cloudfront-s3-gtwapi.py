import boto3

# Initialize the CloudFront client
cloudfront_client = boto3.client('cloudfront')

# Define the S3 bucket as the first origin
s3_bucket = 'your-s3-bucket-name'

# Define the API Gateway as the second origin
api_gateway_domain = 'your-api-gateway-domain'

# Create a CloudFront distribution configuration
distribution_config = {
    'CallerReference': 'unique-reference-string',
    'Origins': {
        'Quantity': 2,
        'Items': [
            {
                'Id': 'S3-Origin',
                'DomainName': f'{s3_bucket}.s3.amazonaws.com',
                'S3OriginConfig': {
                    'OriginAccessIdentity': ''
                }
            },
            {
                'Id': 'API-Gateway-Origin',
                'DomainName': api_gateway_domain,
                'CustomOriginConfig': {
                    'HTTPPort': 80,
                    'HTTPSPort': 443,
                    'OriginProtocolPolicy': 'https-only'
                }
            }
        ]
    },
    'DefaultCacheBehavior': {
        'TargetOriginId': 'S3-Origin',
        'ForwardedValues': {
            'QueryString': False,
            'Cookies': {
                'Forward': 'none'
            }
        },
        'ViewerProtocolPolicy': 'redirect-to-https',
        'MinTTL': 0
    },
    'CacheBehaviors': {
        'Quantity': 1,
        'Items': [
            {
                'PathPattern': '/api/*',
                'TargetOriginId': 'API-Gateway-Origin',
                'ViewerProtocolPolicy': 'https-only',
                'ForwardedValues': {
                    'QueryString': True,
                    'Cookies': {
                        'Forward': 'none'
                    }
                },
                'MinTTL': 3600
            }
        ]
    },
    'Comment': 'Complex CloudFront Distribution',
    'Enabled': True,
    'PriceClass': 'PriceClass_100'
}

# Create the CloudFront distribution
response = cloudfront_client.create_distribution(DistributionConfig=distribution_config)

# Print the distribution information
print("CloudFront Distribution created with Id:", response['Distribution']['Id'])
