import subprocess
import os
import json
import sys


def execute_command(command):
    process=subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if process.returncode == 0:
        pass
    else:
        print('An error ocurred')
    return process

def auth_gcloud():
    command = 'gcloud auth activate-service-account --key-file=service-account.json'
    if os.path.exists('service-account.json'):
        authg = execute_command(command)
        if authg.returncode == 0:
            print(authg.stdout.decode('utf-8'))
        else:
            print(authg.stdout.decode('utf-8'))
    else: 
        print('Need account json file saved in service-account.json')

def sele_proj(project_dict):
    command = 'gcloud config unset project'
    execute_command(command)
    sel_project = int(input("Select project(Insert number):"))
    if isinstance(sel_project, int):
        selected_project = project_dict[sel_project]
        print("You have selected: ", selected_project)
        try:
            command = f'gcloud config set project "{selected_project}"'
            proj = execute_command(command)
            print(proj.stdout.decode('utf-8'))
        except:
            print("An error ocurred")
            sys.exit(1)

def projects_list():
    project_dict ={}
    print('Obtaining projects...')
    command = 'gcloud projects list --format=json'
    plist = execute_command(command)
    if plist.returncode == 0:
        projects = plist.stdout
        projectst = json.loads(projects.decode('utf-8'))
        savedlist = input('Do you want to save projects list to a file(Y/N)?')
        if savedlist.upper() == "Y":
            with open('project-list.csv', "w+") as savedp:
                projectstxt = 'name' + ',' + 'created time' + ',' + 'status' + ',' + 'owner' + '\n'
                savedp.write(projectstxt)
                for project in projectst:
                    if 'labels' in project:
                        if 'owner' in project['labels']:
                            projectstxt = project['name'] + ',' + project['createTime'] + ',' + project['lifecycleState'] + ',' + project['labels']['owner'] + '\n'
                            savedp.write(projectstxt)
                    else:
                        projectstxt = project['name'] + ',' + project['createTime'] + ',' + project['lifecycleState'] + '\n'
                        savedp.write(projectstxt)
                print('file saved as project-list.txt')
        i=0 
        print('Projects list:')
        for project in projectst:
            project_dict[i] = project["name"]
            i += 1 
        for order, elem in project_dict.items():
            print(order, elem)
        print("There are ", i , " projects")
        try:
            sele_proj(project_dict)
        except:
            print("select valid value for project")
            sele_proj(project_dict)

def get_logging_list():
    log_list = {}
    command = "gcloud logging logs list"
    loglist = execute_command(command)
    if loglist.returncode == 0:
        loglisting = loglist.stdout.decode('utf-8').split('\n')
        i = 0
        for log in loglisting:
            log_list[i]= log
            i += 1
        del log_list[0]
        del log_list[(len(log_list))]
        print("Select log: ")
        for order, elem in log_list.items():
            print(order , elem)

def main():
    auth_gcloud()
    projects_list()
    get_logging_list()

if __name__ == '__main__':
    print('Authenticating...')
    main()