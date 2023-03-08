import json
import boto3
import base64
import os

s3=boto3.client('s3')


def lambda_handler(event, context):
    
    key = event['s3_key']
    bucket = event['s3_bucket']
    
    
    file_path = os.path.join('/tmp', 'image.png')
    with open(file_path, 'wb') as f:
        s3.download_fileobj(bucket, key, f)
    
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())
        
    print("Event:", event.keys())
    print('Image data ',image_data)
    
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2023-03-07-14-46-40-176'

runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    
    data = json.loads(json.dumps(event))
    image = base64.b64decode(event['image_data'])
    
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT,
                                       ContentType='image/png',
                                       Body=image)

    
    # Make a prediction:
    # inferences = predictor.predict(image)
    result = json.loads(response['Body'].read().decode())
    
    # We return the data back to the Step Function    
    event["inferences"] = result
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }

THRESHOLD = .93

def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event['inferences']
    
    #inferences = json.loads(inferences)
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = [x for x in inferences if x>THRESHOLD]
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }