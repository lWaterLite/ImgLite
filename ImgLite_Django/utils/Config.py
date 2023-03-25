"""
Project Configuration

DatabaseInfo:
    dict, the Configuration of database, see more in https://docs.djangoproject.com/en/4.1/ref/databases/

WhitelistSite:
    list, the whitelist site, add your own site here.

StaticPath:
    string, the absolute disk path where all images stored, change it to your own.

RawUrlPrefix:
    string, your serve url prefix.
"""
DatabaseInfo = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'imglite',
    'HOST': 'localhost',
    'PORT': 3306,
    'USER': 'root',
    'PASSWORD': 'root'
}

WhitelistSite = [
    'http://localhost:8080',
    'http://127.0.0.1:8080'
]

StaticPath = r'C:/work/Program_space/Git/ImgLite/static'

RawUrlPrefix = 'Http://localhost:8080/api/r/'
