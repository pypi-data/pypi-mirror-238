from Dxr_file.dxr_file import *

smb = dxr_file()
current_dir = os.path.dirname(os.path.abspath(__file__))
r_url = smb.upload('dxr', 'test', current_dir, 'requirements.txt')
print(r_url)