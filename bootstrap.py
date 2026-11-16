"""Generic private-ZIP bootstrap; contains no workflow, token, or model weights."""
import os,pathlib,subprocess,tempfile,zipfile
from urllib.parse import urlsplit

def main():
    token=os.environ.get('HF_TOKEN','')
    url=os.environ.get('H3_SETUP_URL','')
    if not token or 'RUNPOD_SECRET' in token:
        raise SystemExit('HF_TOKEN is missing or its RunPod secret was not resolved.')
    parsed=urlsplit(url)
    if parsed.scheme!='https' or parsed.hostname!='huggingface.co':
        raise SystemExit('H3_SETUP_URL must be an HTTPS huggingface.co URL.')
    if any(c in token for c in '\r\n"\\'):
        raise SystemExit('HF_TOKEN has an unexpected format.')
    root=pathlib.Path(tempfile.mkdtemp(prefix='h3-bootstrap-'))
    archive=root/'setup.zip'
    print('Downloading private H3 setup package...',flush=True)
    subprocess.run(['curl','--config','-','--fail','--location','--retry','5',
        '--connect-timeout','30','--output',str(archive),url],
        input='header = "Authorization: Bearer '+token+'"\n',text=True,check=True)
    with zipfile.ZipFile(archive) as z:
        for item in z.infolist():
            dest=(root/item.filename).resolve()
            if not dest.is_relative_to(root.resolve()):
                raise SystemExit('Unsafe path in setup archive.')
        z.extractall(root)
    boot=root/'H3_RunPod_Setup/boot.py'
    if not boot.is_file():raise SystemExit('ZIP is missing H3_RunPod_Setup/boot.py.')
    print('Starting H3-aware RunPod launcher...',flush=True)
    os.execvp('python3.12',['python3.12',str(boot)])

if __name__=='__main__':main()
