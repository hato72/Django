import requests

url = 'http://localhost:8000/api_token_auth/'

response = requests.post(url,data = {
    "username":'hato3',"password":"12345678",
})
print(response.text)
# {"token":"5f41ac5595ddb5277a3e160e7c0bf9fb0c99e145"}

url = 'http://localhost:8000/apiv2/product/'

token = response.json().get("token")
print(token)
response = requests.post(url,data = {
    "name":'Product 1',"price":"10000","user":3
}, headers={"Authentication":f"Token {token}"})
print(response.text)