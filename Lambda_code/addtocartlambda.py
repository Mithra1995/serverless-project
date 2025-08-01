import boto3
import json
import uuid
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Cart')  # Ensure Cart table has Partition key: user_id, Sort key: product_id

def lambda_handler(event, context):
    try:
        print("Received event:", event)

        # Parse body
        body = json.loads(event.get('body', '{}'))

        # Validate required fields
        required_fields = ['user_id', 'product_id', 'product_name', 'price']
        missing_fields = [field for field in required_fields if field not in body]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Extract and convert
        user_id = str(body['user_id'])
        product_id = str(body['product_id'])
        product_name = str(body['product_name'])
        price = Decimal(str(body['price']))  # Avoid float issues

        # Check if product already in cart
        existing = table.get_item(
            Key={
                'user_id': user_id,
                'product_id': product_id
            }
        )

        if 'Item' in existing:
            # Update existing item: increment quantity and price
            current_quantity = int(existing['Item'].get('quantity', 1))
            new_quantity = current_quantity + 1
            new_price = price * new_quantity

            table.update_item(
                Key={
                    'user_id': user_id,
                    'product_id': product_id
                },
                UpdateExpression="SET quantity = :q, price = :p",
                ExpressionAttributeValues={
                    ':q': new_quantity,
                    ':p': new_price
                }
            )

            message = f"Updated quantity to {new_quantity} for {product_name}"

        else:
            # Insert new item
            table.put_item(
                Item={
                    'user_id': user_id,
                    'product_id': product_id,
                    'product_name': product_name,
                    'price': price,
                    'quantity': 1
                }
            )
            message = f"Added new product {product_name} to cart"

        # Success response
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({'message': message})
        }

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({'error': 'Failed to add item to cart', 'details': str(e)})
        }
