## File optimizer 

A project to help developers fix disasters or simply reduce space and optimise files.

Providers support: 
* AWS S3

### Local use

1. Clone repository.
2. Copy `.env.example` and paste, rename to `.env`.
3. Change env values to your own.
4. Install dependencies.
5. In main.py you should change the bucket name
6. And run with `python3 src/main.py`


### Todo:

* Make multiple provider
  * Local process
  * Azure bucket
  * Google storage
  *  etc
*  Think a safy way to pass credentials
* Add more files formats.
  * PDF
* Find duplicates
* Add dependencies manager