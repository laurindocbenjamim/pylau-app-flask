



token1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdEBnbWFpbC5jb20iLCJleHAiOjE3MjgyMjA4OTYsIm5iZiI6MTcyODEzNDQ5Nn0.Mr8oIxkhSJXD2qt20vHYnRyjdecNIy6vUhFhwQ5j2yk"
token2 ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdEBnbWFpbC5jb20iLCJleHAiOjE3MjgyMjA4OTYsIm5iZiI6MTcyODEzNDQ5Nn0.Mr8oIxkhSJXD2qt20vHYnRyjdecNIy6vUhFhwQ5j2yk"

if token2 == token1:
    print("Equals")
else:
    print("different")
name ="Python Basic Level".split(' ')
#s = next(['' for i in name])
i=''

for k,l in enumerate(name):
    i+= str(l[0])
    print(i)


test = "ola mundo.png"
if ['.jpg','.png'] in test:
    print("It's in")
else:
    print("It's not")
