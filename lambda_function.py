import json
import boto3
import uuid
from datetime import datetime
import traceback

dynamodb = boto3.resource('dynamodb')
tabela = dynamodb.Table('Workouts')

def lambda_handler(event, context):
    print("EVENTO RECEBIDO:", json.dumps(event))  # Debugzinho maroto

    try:
        route_key = event['requestContext']['routeKey']

        if route_key == 'GET /workouts':
            response = tabela.scan()
            treinos = response.get('Items', [])
            return {
                'statusCode': 200,
                'body': json.dumps(treinos, default=str)
            }

        elif route_key == 'POST /workouts':
            body = json.loads(event['body'])

            workout_id = str(uuid.uuid4())
            user_id = body['user_id']
            data = body.get('data') or datetime.utcnow().isoformat()
            tipo = body['tipo']
            exercicios = body['exercicios']

            treino = {
                'id': workout_id,
                'user_id': user_id,
                'data': data,
                'tipo': tipo,
                'exercicios': exercicios
            }

            tabela.put_item(Item=treino)

            return {
                'statusCode': 201,
                'body': json.dumps({
                    'message': 'Treino salvo com sucesso!',
                    'id': workout_id,
                    'treino': treino
                }, default=str)
            }

        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'mensagem': 'Rota não encontrada'})
            }

    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Campo obrigatório ausente: {str(e)}'})
        }

    except Exception as e:
        print("ERRO:", str(e))
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
