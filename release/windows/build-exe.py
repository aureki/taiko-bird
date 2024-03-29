import subprocess
from zipfile import ZipFile
import os
from pathlib import Path
import shutil
import urllib.request
import sys

this_directory = Path(__file__).parent
love_files_directory = this_directory / 'love-files'
resource_hacker_directory = this_directory / 'resource-hacker'


def clean_directory(directory: Path):
    try:
        shutil.rmtree(directory)
    except:
        pass
    
    try:
        os.makedirs(directory)
    except:
        pass


def download_love_files():
    url = 'https://github.com/love2d/love/releases/download/11.4/love-11.4-win64.zip'
    output_file = this_directory / 'love-11.4-win64.zip'

    if not output_file.exists():
        # Download do love.exe sem módulos externos com Windows
        with urllib.request.urlopen(url) as response, open(output_file, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            out_file.flush()
            out_file.close()

    clean_directory(love_files_directory)
    
    # Extração do love.exe sem a pasta
    with ZipFile(output_file) as zip_file:
        for member in zip_file.namelist():
            filename = os.path.basename(member)
            # skip directories
            if not filename:
                continue
        
            # copy file (taken from zipfile's extract)
            source = zip_file.open(member)
            target = open(os.path.join(love_files_directory, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)
        
def download_resource_hacker():
    url = 'http://www.angusj.com/resourcehacker/resource_hacker.zip'
    output_file = this_directory / 'resource_hacker.zip'

    if not output_file.exists():
        with urllib.request.urlopen(url) as response, open(output_file, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            out_file.flush()
            out_file.close()
            
    clean_directory(resource_hacker_directory)
    
    # Extração do resource_hacker.exe
    with ZipFile(output_file, 'r') as zip:
        zip.extractall(resource_hacker_directory)

def download_rcedit():
    url = 'https://github.com/electron/rcedit/releases/download/v1.1.1/rcedit-x64.exe'
    output_file = this_directory / 'rcedit-x64.exe'

    if not output_file.exists():
        with urllib.request.urlopen(url) as response, open(output_file, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
            out_file.flush()
            out_file.close()

def create_game_love():
    with ZipFile(this_directory / 'taikobird.love', 'w') as zip:
        # Pasta com os arquivos do jogo
        game_directory = Path(__file__).parent.parent.parent

        ignored_files_and_folders = [
            game_directory / '.git',
            game_directory / '.gitignore',
            game_directory / 'release',
        ]

        for folder, subfolders, files in os.walk(game_directory):
            for file in files:
                filepath = os.path.join(folder, file)
                unsafe = False
                for ignored_file_and_folder in ignored_files_and_folders:
                    # Verifica se o arquivo atual é igual ao ignorado
                    if Path(filepath).absolute() == ignored_file_and_folder.absolute():
                        unsafe = True
                        print('Ignoring file:', filepath) # debug
                    # Verifica se o arquivo atual está dentro de uma das pastas ignoradas
                    if ignored_file_and_folder.absolute() in Path(filepath).absolute().parents:
                        unsafe = True
                        print('Ignoring file:', filepath) # debug
                        
                if not unsafe:
                    new_filepath = filepath.replace(str(game_directory), '')
                    print('Writing file', filepath, 'to', new_filepath)
                    zip.write(filepath, new_filepath)
                else:
                    continue

def create_game_exe():
    love_exe = love_files_directory / 'love.exe'
    game_exe = love_files_directory / 'taikobird.exe'
    taikobird_love = this_directory / 'taikobird.love'

    with open(game_exe, 'wb') as game_file:
        # Escrever conteudos do love.exe e do taikobird.love dentro do taikobird.exe
        with open(love_exe, 'rb') as love_file:
            game_file.write(love_file.read())
            
        with open(taikobird_love, 'rb') as taikobird_love_file:
            game_file.write(taikobird_love_file.read())

def change_game_icon():
    rcedit_exe = this_directory / 'rcedit-x64.exe'
    game_exe = love_files_directory / 'taikobird.exe'
    icon_path = this_directory / 'taikobird.ico'
    command_prefix = []
    additional_envs = {}

    if sys.platform == 'linux':
        # resource_hacker_exe = subprocess.check_output(['winepath', '-w', str(resource_hacker_directory)]).strip()
        game_exe = subprocess.check_output(['winepath', '-w', str(game_exe)], text=True).strip()
        icon_path = subprocess.check_output(['winepath', '-w', str(icon_path)], text=True).strip()
        command_prefix = ['wine']
        additional_envs = {'WINEARCH': 'win64'}

    # change icon with Resource Hacker
    subprocess.run(command_prefix + [
        rcedit_exe,
        game_exe,
        '--set-icon', icon_path,
    ], env={**os.environ, **additional_envs})

def zip_love_files():
    with ZipFile(this_directory / 'taiko-bird-win64.zip', 'w') as zip:
        for folder, subfolders, files in os.walk(love_files_directory):
            for file in files:
                filepath = os.path.join(folder, file)
                new_filepath = filepath.replace(str(love_files_directory), '')
                zip.write(filepath, new_filepath)

def main():
    download_love_files()
    download_rcedit()
    create_game_love()
    create_game_exe()
    change_game_icon()
    zip_love_files()

if __name__ == "__main__":
    main()
