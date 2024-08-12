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

## Disclaimer

This tool is developed specifically for penetration testers and cybersecurity professionals. It is intended solely for demonstrational and research purposes. The use of this tool must comply with all applicable laws and regulations. Unauthorized use of this tool for malicious purposes, including but not limited to unauthorized system access or data breaches, is strictly prohibited. The creators and distributors of this tool are not responsible for any misuse or damage caused by its use. Always ensure that you have proper authorization before conducting any security testing activities.
