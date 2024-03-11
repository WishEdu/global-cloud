# WISH EDU CDN System



## Routes
### GET files
- Static  files (can be added only by developers ftps/ssh direct sending on server)
    ```
    /assets/static/*
    {
    }
    ```
- Other files
    ```
    /assets/<owner_type: str>/<owner_id: int>/<file_type: str>/<file_unique_id: str>.ext
    ```
    ##### Url parts
    ```
    {
        owner_type: user, group, etc.
        file_type: avatar, attachment, logo, etc.
        file_unique_id: can become known only from backend
    }
    ```
    ##### Requirements:
    ```
    {
        max_size: 10MB, (.webp max size = 100KB)
        ext: any, but images only in .webp (and sometimes .gif for groups)
    }
    ```
##### Respone:
- If everything's OK, and file exists and successfully getted:
```<binary file>, 200```
- If y0u tried to use any methods but GET:
```<default error page>, 405```
- If there's any problems:
```<default error page>, 40x```
    

### Backend only(whitelist) api for files manipulating and id finding out
```
/api
```
#### GET and DELETE
##### Querry params:
```python
{
    "file_id": int # file id on cdn's db(will be finded out by post method)
}
```
##### Response:
- GET, if everything's OK:
```<file_url_on_cdn: str>, 200```
- DELETE, if everything's OK:
```'OK', 200```
- If there's no file with such file_id:
```{'errorMessage': 'No file with such file_id'}, 400```
- If there's some inner SQL error:
```{'errorMessage': 'SQL error'}, 500```
- If there's by some reason no such file on server(but exists in db):
```{'errorMessage': 'No such file'}, 500```
#### POST
##### Querry params:
```python
{
    "file_owner": str, # user, group, etc.
    "file_owner_id": int,
    "file_type": str # attachment, avatar, logo, etc.
}
```
##### Body:
A binary file that complies with the requirements of the GET clause
##### Respone:
- If everything's OK, and file successfully loaded and saved:
```<file's id on cdn's db>, 200```
- If someting goes wrong(for example, wrong querry params names):
```<default error page>, 40x```
---
### Route for finding out users' avatars or groups' logos
```
/api/avalogo
```
#### GET
##### Querry params:
```python
# same as in the GET files or API POST paragraphs
{
    "owner_type": str, 
    "owner_id": int
} 
```
##### Response
- GET, if everything's OK:
```<file_url_on_cdn: str>, 200```
- If there's no such owner(combination of type(user, group) and id):
```{'errorMessage': 'No such owner'}, 400```
- If there's some inner SQL error:
```{'errorMessage': 'SQL error'}, 500```
- If there's by some reason no such file on server(but exists in db):
```{'errorMessage': 'No such file'}, 500```