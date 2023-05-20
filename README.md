---
  GETTING STARTED
---

1 - Install requirements
  pip install -r requirements.txt
 
2 - Runserver on port 8000

    python manage.py runserver
    
    http://127.0.0.1:8000/
    
    
---
  ENDPOINTS
---

- /
```
  Acebt only GET request
```

- /audio-api/
```
  GET request will return a list of audio elements
  POST request for create a new audio element 
  /audio-api.json will return response on json format
```

- /audio-api/:id/
```
  GET request will return a single audio elements
  POST request for updating the audio element 
  DELETE request for deleting the audio element 
  /audio-api/:id.json will return response on json format
```