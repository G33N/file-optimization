## File optimizer 

A project to help developers fix disasters or simply reduce space and optimise files.

Providers support: 
* AWS S3

### Local use S3 bucket optimization

1. Clone repository.
2. Run a virtual environmnt 
```
python3 -m venv venv                    
source venv/bin/activate
```
3. Install dependencies. `pip install -r requirements.txt`
4. And run with `python3 src/cli_menu.py`
5. Choose a option: 
   1. Image optimization
   2. Find duplicates
6. The CLI will ask you for your aws credentials and bucket name and run.


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
* Add dependencies manager

19110 rows -> clean broken files ->  rows