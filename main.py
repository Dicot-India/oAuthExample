import requests
import pathlib 
def upload_data(data, server_url, endpoint):
  """Uploads data to a server with ExpressJS.

  Args:
    data: The data to upload.
    server_url: The URL of the server.
    endpoint: The endpoint on the server to upload the data to.
    header:The header is take authorization token
  """
  
  TOKEN=data['accessToken']
  request={'Project_id':'eb77307d-c032-4dcf-8540-12381d169e15'}
  response = requests.post(f"{server_url}/{endpoint}?token="+TOKEN+"&projectID=eb77307d-c032-4dcf-8540-12381d169e15", data=request,headers={"Authorization": f"Bearer {TOKEN}"})
  print(response)

  if response.status_code == 200:
    # The data was uploaded successfully.
    print("Data uploaded successfully.")
  else:
    # There was an error uploading the data.
    raise Exception(f"Failed to upload data: {response.status_code} {response.reason}")

def LoginUser(data,serve_url,endpoint):
  print(serve_url+endpoint)
  response=requests.post(serve_url+endpoint,data=data).json()
  env_path=pathlib.Path(".env")
  if not env_path.exists():
    env_path.touch()
  
  with open(env_path,'w') as file:
    file.write("AUTH_CODE="+response['authcode'])
    file.close()

  resp=requests.get(serve_url+'user/token?authCode='+response['authcode']).json()

 
  refreshTOken(serve_url,'generateToken',{"refreshToken":resp['refreshToken']})


def refreshTOken(serve_url,endpoint,data):
  resp=requests.get(serve_url+endpoint,data=data).json()

  upload_data(resp,'http://localhost:8080','db/get-data')
  

# Example usage:

# data = {"Project_id":"d0ce6fe1-eb41-49ff-92cb-e067234c11f0","name": "John Doe", "age": 30}

server_url = "http://localhost:8080/auth/"
endpoint='userLogin'
data={"email":"nandan@dicot.tech","password":"dicot99","grantType":"API_","successType":"online"}
LoginUser(data,server_url,endpoint)


