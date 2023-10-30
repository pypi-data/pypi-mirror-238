import os
import pkg_resources
import shutil
import subprocess
from colorama import Fore, init, Style

FILES_TO_COPY = ['.pre-commit-config.yaml', 'pylintrc', 'mypy.ini']

def find_git_folder(start_path):
    current_path = os.path.abspath(start_path)

    while current_path != '/':  # or any other condition to stop the search
        git_folder = os.path.join(current_path, '.git')
        if os.path.isdir(git_folder):
            return git_folder.replace(".git", "")
        else:
            current_path = os.path.dirname(current_path)

    return None  # No .git folder found

def main():
    init(autoreset=True)

    print(Style.BRIGHT + Fore.GREEN + "Installing Paraty Pre-Commit...")
    project_path = os.getcwd()
    project_path = find_git_folder(project_path)

    if not project_path:
        exit(0)

    package_name = 'paraty_commit'
    package_path = pkg_resources.resource_filename(package_name, '')

    files = os.listdir(package_path)
    files = [file for file in files if file in FILES_TO_COPY]
    files = [file for file in files if os.path.isfile(os.path.join(package_path, file))]

    print(Style.BRIGHT + Fore.GREEN + f"Package Path: {package_path}")
    print(Style.BRIGHT + Fore.GREEN + f"Project Path: {project_path}")

    for file in files:
        file_name_path = os.path.join(package_path, file)
        file_name_project_path = os.path.join(project_path, file)
        shutil.copy(file_name_path, file_name_project_path)
        print(Fore.GREEN + f"Added file: {file}")

    execute_command("pip install pre-commit==2.9.2")
    print('find "'+project_path+'" -type f -name ".pre-commit-config.yaml" -exec git add {} \;')
    execute_command('find "'+project_path+'" -type f -name ".pre-commit-config.yaml" -exec git add {} \;')
    execute_command("pre-commit autoupdate --bleeding-edge")
    execute_command("pre-commit install")
    execute_command("pip install pylint==2.15.10")

    print(Style.BRIGHT + Fore.GREEN + "Paraty Pre-Commit Installed!!")


def execute_command(comando):
    print(Style.BRIGHT + Fore.GREEN + f">> {comando}")
    proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    salida_stdout, salida_stderr = proceso.communicate()
    codigo_salida = proceso.returncode
    if salida_stderr:
        print(salida_stderr.decode('utf-8'))
        print("<<<<<<<<<<<<<<<<<<<<<<<")
    if salida_stdout:
        print(salida_stdout.decode('utf-8'))
        print("<<<<<<<<<<<<<<<<<<<<<<<")

    if proceso.returncode != 0:
        print(Style.BRIGHT + Fore.RED + "Installation Aborted!")
        exit(-1)

if __name__ == '__main__':
   main()