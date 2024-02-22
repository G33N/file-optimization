## File optimizer 

A project to help developers fix disasters or simply reduce space and optimise files.

Providers support: 
* AWS S3

### Local use S3 bucket optimization

1. Clone repository.
4. Install dependencies.
5. And run with `python3 src/main.py`
6. The CLI will ask you for your aws credentials and bucket name


### Tips 

You can check the S3 bucket size before and after execute with 

`aws s3 ls s3://bucket-name --recursive --human-readable --summarize`


### Todo:

* Make multiple provider
  * Local process
  * Azure bucket
  * Google storage
  *  etc
* Add more files formats.
  * PDF
* Find duplicates
* Add dependencies manager