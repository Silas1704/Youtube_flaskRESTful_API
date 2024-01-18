import requests
#this is client

BASE="http://127.0.0.1:5000/"

# data=[{"name": "isha","likes":18,"views":100},
#      {"name": "baby","likes":19,"views":1000},
#       {"name": " face","likes":23,"views":90},
#       {"name": "adiyua e","likes":8,"views":55}]

# for i in range(len(data)):
#     response=requests.put(BASE+"video/"+str(i),data[i])
#     print(response.json())

#input()

response=requests.patch(BASE+"video/2",{"views":99})
print(response.json())

#response=requests.put(BASE+"video/1",{"name": "pussy face","likes":19,"views":100})
#print(response.json())


#response=requests.get(BASE+"video/2")
#print(response.json())
 