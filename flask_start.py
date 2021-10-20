from flask import Flask,render_template,request
import boto3

def dynamo_create(userId,amount,years,rate):
    # 1 - Create Client
    ddb = boto3.resource('dynamodb',
                         endpoint_url='http://localhost:8000',
                         region_name='dummy',
                         aws_access_key_id='dummy',
                         aws_secret_access_key='dummy')
    # 2 - Create the Table
    try:
        ddb.create_table(TableName='Users',
                        AttributeDefinitions=[
                            {
                                'AttributeName': 'UserId',
                                'AttributeType': 'S'
                            }
                        ],
                        KeySchema=[
                            {
                                'AttributeName': 'UserId',
                                'KeyType': 'HASH'
                            }
                        ],
                        ProvisionedThroughput= {
                            'ReadCapacityUnits': 10,
                            'WriteCapacityUnits': 10
                        }
                        )
        print('\nSuccessfully created Table\n')
    except:
        print("\nInserting new record !!!\n")

    table = ddb.Table('Users')
     
    value=str(round(float(amount)*(( 1 + float(rate)/100)**int(years)))) 
    input = {'UserId': userId, 'Amount': amount,'Years': years,'Interest': rate,"Final Amount to be received":value}
    #input = {'UserId': userId, 'Amount': amount,'Years': years,'Interest': rate}
    #3 - Insert Data
    table.put_item(Item=input)
    print('Successfully inserted item\n')

    #4 - Scan Table
    scanResponse = table.scan(TableName='Users')
    items = scanResponse['Items']
    print("Records in the table\n")
    for item in items:
        print(item)
    print('\n')
    return input

app = Flask(__name__)
 
@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        user_data=form_data.to_dict()
        # print("Transac:",user_data.get("Transaction_ID"),"amount:",user_data.get("Amount"))
        temp=dynamo_create(user_data.get("UserId"),user_data.get("Amount"),user_data.get("Years"),user_data.get("Interest"))
        return render_template('data.html',form_data = temp)
 
 
app.run(host='localhost', port=5000)        
