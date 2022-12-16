import json
import sys
import boto3

try:
    modo = sys.argv[1]
except:
    modo = 'editar'

aws_profile = 'rocha-dev-legacy'
aws_region = 'us-east-1'

#filtros
filter_key='product'
filter_value=['appstore', 'AppStore']

#valores para alterar
target_key='escalationList'
target_value='ecsongdo@uolinc.com, l-devops-cupertino@uolinc.com'


#########################################################################
#inicia a sessao
session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
client = session.client('resourcegroupstaggingapi')

#Lista as tags
response = client.get_resources(

    TagFilters=[
        {
            'Key': filter_key,
            'Values': filter_value
        },
    ]
)
     
dictionary = json.dumps(response)
dictionary2 = json.loads(dictionary)
dic = json.dumps(dictionary2['ResourceTagMappingList'])
recursos = json.loads(dic)

# comeca a percorrer o array para fazer o update
for recurso in recursos:
    json_tags = json.dumps(recurso['Tags'])
    tags = json.loads(json_tags)
    for tag in tags:
            
        if tag['Key'] == filter_key:

            print(f"ARN['ResourceARN'] = {recurso['ResourceARN']}     KEY['{filter_key}'] = {tag['Value']} ")
                        
            if modo == 'editar':
                response_tag = client.tag_resources(
                    ResourceARNList=[
                        recurso['ResourceARN'],
                    ],
                    Tags={
                        target_key: target_value 
                    }
                )
                if '400' in str(response_tag):  
                    print(response_tag)

            elif modo == 'remover':
                response = client.untag_resources(
                    ResourceARNList=[
                        recurso['ResourceARN'],
                    ],
                    TagKeys=[
                        target_key
                    ]
                )