The forum allows API access, if I generate a token using the Admin page (indicated by `XXXXX` in examples).

Using the Plugins Rest API To Text, able to verify:
```
GET https://community.notepad-plus-plus.org/api/v3/users/3841
**Headers**
Content-Type: application/json
Accept: application/json
Authorization: Bearer XXXXX
```
will return with JSON about me

and 
```
PUT https://community.notepad-plus-plus.org/api/v3/users/3841
**Headers**
Content-Type: application/json
Accept: application/json
Authorization: Bearer XXXXX
**Body**
{
    "website": "https://github.com/pryrt?tab=repositories"
}
```
will update my website.  

So I need to prefix the endpoints they list in the docs with `/api/v3`

