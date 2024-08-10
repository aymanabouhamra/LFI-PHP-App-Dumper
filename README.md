# LFI-PHP-App-Dumper
This will extract all the source code of a PHP app if you have found an LFI (Local File Inclusion)

## Here's the steps that you need to do
1. Modify the lfi.py file. Update the single function that is there to implement the LFI scenario that you found
2. Run the dumper.py !


We have set an example using the ***Acunetix acuart*** app.
http://testphp.vulnweb.com/

```
python dumper.py http://testphp.vulnweb.com -www /hj/var/www/
```

## Parameters

| Name | Description | Default | Example |
| --- | --- | --- | --- |
| Base_url | This will contain the base url of the web app |NA | http://testphp.vulnweb.com |
| indexFile | This is the index PHP file / starting point | index.php | index.php |
| www | This is the absolute directory on the server that is serving the PHP app | /var/www/ | /var/www/my-app/
| output | This is the directory in which the PHP source code files will be saved in | output (in the current working directory) | /home/user/Workspaces/app/