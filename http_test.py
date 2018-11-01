import requests;

result = requests.post('http://35.200.117.1:8080/control.jsp?type=reservation&action=select&from=mobile&userId=ID1234')
print(result.text)
