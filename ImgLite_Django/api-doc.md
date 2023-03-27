# api document

---

## Catalog

### authentication

* [/api/auth/login](#/api/auth/login)
* [/api/auth/register](#/api/auth/register)
* [/api/token](#/api/token)

### image

* [/api/image/images](#/api/image/images)
* [/api/image/upload](#/api/image/upload)
* [/api/image/page](#/api/image/page)
* [/api/image/delete](#/api/image/delete)
* [/api/image/thumb/(str:imgUUID)](#/api/image/thumb/(str:imgUUID))
* [/api/r/(str:imgUUID)](#/api/r/(str:imgUUID))
* [/api/d/(str:imgUUID)](#/api/d/(str:imgUUID))

### statement

* [/api/state/csv](#/api/state/csv)
* [/api/state/excel](#/api/state/excel)

---

## Details

Symbol definition: A param is necessary when bold. A word is a static value when italic.

### /api/auth/login

To log into site.

* Method Limitation: GET
* Params: 
    * **userAccount**: string, user account, RSA encrypted.
    * **userPassword**: string, user password, RSA encrypted.
* Response: application/json
    * success: json object
      * userUUID: string, user uuid, RSA encrypted.
      * status: string, _true_.
    * failed: json object
      * message: string, error message.
      * status: string, _false_.

### /api/auth/register

To register for an account.

* Method Limitation: POST
* Params:
  * **userAccount**: string, user account, RSA encrypted.
  * **userPassword**: string, user password, RSA encrypted.
  * **inviteCode**: string, invite code.
* Response: application/json, json object
  * message: string, message of success info or error info.
  * status: string, _true_ when success, _false_ otherwise.

### /api/token

To get a csrf token.

* Response: application/json, json object
  * message: string, _success_.
* Set-Cookie: csrftoken.

### /api/image/images

To get users' image info, page based.

* Method Limitation: GET
* Params:
  * **userUUID**: string, user uuid, RSA encrypted.
  * page: string, page number, default to 1 if not be set.
* Response: application/json
  * success: json array, for each element, it's json object.
    * imgUUID: string, image uuid.
    * imgFilename: string, image filename.
    * imgUploadDate: string, image upload date, 'YYYY-MM-DD'.
  * failed: json object
    * message: string, error message.

### /api/image/upload

To upload a image.

* Method Limitation: POST
* Params: form-data
  * **userUUID**: string, user uuid, RSA encrypted.
  * **file**: binary, image file.
* Response: application/json, json object
  * message: string, _success_.
  * imgUUID: string, image uuid.
  * imgFilename: string, image filename.

### /api/image/page

To get users' image data page number.

* Method Limitation: GET.
* Params:
  * **userUUID**: string, user uuid, RSA encrypted.
* Response: application/json, json object.
  * pageCount: int, page number.

### /api/image/delete

To delete a image.

* Method Limitation: DELETE.
* Params:
  * **imgUUID**: string, image uuid.
  * **userUUID**: string, user uuid, RSA encrypted.
* Response: application/json, json object.
  * message: string, message of success info or error info.

### /api/image/thumb/(str:imgUUID)

To get image thumb.

* Method Limitation: GET.
* Params:
  * **imgUUID**: string, image uuid.
* Response: image/type, with image binary.

### /api/r/(str:imgUUID)

To get image binary for direct link.

* Method Limitation: GET.
* Params: 
  * **imgUUID**: string, image uuid.
* Response: image/type, with image binary.

### /api/d/(str:imgUUID)

To download image file.

* Method Limitation: GET
* Params:
  * **imgUUID**: string, image uuid.
* Response: application/octet-stream, with image file.

### /api/state/csv

To download csv file of all image info

* Method Limitation: GET.
* Params:
  * userUUID: string, user uuid, RSA encrypted.
* Response: application/octet-stream, with csv file.

### /api/state/excel

To download Excel file of all image info

* Method Limitation: GET.
* Params:
  * userUUID: string, user uuid, RSA encrypted.
* Response: application/octet-stream, with Excel file.