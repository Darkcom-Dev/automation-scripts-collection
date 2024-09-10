#!/usr/bin/env python3

import os
import subprocess
import curses

def create_project(project_name):
    os.mkdir(project_name)
    os.chdir(project_name)
    os.mkdir('src')
    

    with open('main.py','w') as f:
        content = f'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# {project_name}
def main():
    pass

if __name__ == '__main__':
    main()
'''

    with open('Readme.md','w') as f:
        f.write(f'# {project_name}')
    
    with open('requirements.txt','w') as f:
        f.write(f'# {project_name}')

    with open('.gitignore','w') as f:
        content = f'''
venv/
__pycache__/
*.pyc
.env
'''
        f.write(content)

    subprocess.call('python3 -m venv venv', shell=True)
    # subprocess.call('source venv/bin/activate', shell=True)
    subprocess.call('git init', shell=True)

def main(project_name):

    create_project(project_name)
    pass

if __name__ == '__main__':
    print('Creando un proyecto de Python')
    main(input('Cual es el nombre de su proyecto?: '))