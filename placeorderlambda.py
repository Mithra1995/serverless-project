import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
cart_table = dynamodb.Table('Cart')
orders_table = dynamodb.Table('Orders')
products_table = dynamodb.Table('Products')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user_id = body['user_id']
        address = body.get('shipping_address', '')

        # Fetch cart items for the user
        response = cart_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
        )
        cart_items = response.get('Items', [])

        if not cart_items:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*'
                },
                'body': json.dumps({'error': 'Cart is empty'})
            }

        total_amount = Decimal('0.0')
        order_items = []

        # Prepare order details
        for item in cart_items:
            product_id = item['product_id']
            quantity = int(item.get('quantity', 1))

            product_data = products_table.get_item(
                Key={'product_id': product_id}
            ).get('Item')

            if not product_data:
                continue

            price = Decimal(str(product_data.get('price', 0)))
            total_amount += price * quantity

            order_items.append({
                'product_id': product_id,
                'product_name': product_data.get('product_name', ''),
                'quantity': quantity,
                'price': price
            })

        # Generate and store order
        order_id = str(uuid.uuid4())
        orders_table.put_item(
            Item={
                'order_id': order_id,
                'user_id': user_id,
                'order_items': order_items,
                'timestamp': datetime.utcnow().isoformat(),
                'total_amount': total_amount,
                'address': address
            }
        )

        # Clear user's cart
        for item in cart_items:
            cart_table.delete_item(
                Key={
                    'user_id': user_id,
                    'product_id': item['product_id']
                }
            )

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*'
            },
            'body': json.dumps({'message': 'Order placed successfully', 'order_id': order_id})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': '*'
            },
            'body': json.dumps({'error': str(e)})
        }
