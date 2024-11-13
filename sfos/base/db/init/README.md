# Initialization scripts

Files in this folder are run when initializing the database. 

Files should be named as:

``` text
##_init_[name].sql
```

### Name parts

* \#\# - Number indicating priority order. Lower numbers will be run first. Numbers should be padded with leading zeros so all number are the same char length, and executed in the correct order.
* \_init\_ - indicates sql script purpose
* [name] - A name indicating the script purpose.
* .sql - Files with any other extension will be ignored.