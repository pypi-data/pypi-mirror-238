import argparse
import os
from datetime import datetime
import subprocess
import json
import shutil
import sys
import re
from .version import __version__

def create_labnotebook(name):
    """
    This function creates a new labnotebook. Thes structure is stored in the newly created .labnotebook folder.
    """

    # 1. Check if .git folder is present
    if not os.path.exists(".git"):
        print("Error: There is no .git folder in the current working directory.")
        print("Please go to the folder where .git is to create a new notebook in the same folder or run 'git init'.")
        return
    pass

    # 2. Create .labnotebook directory if it doesn't exist, otherwise return an error
    try:
        os.makedirs(".labnotebook")
    except OSError:
        print(".labnotebook folder is already present. If you want to create a new .labnotebook directory, you have to firstly delete it.")
        return

    # 3. Get useful variables
    today = datetime.now().strftime('%Y-%m-%d')
    aut = subprocess.check_output(["git", "config", "--get", "user.name"], universal_newlines = True).strip()
    red = '\033[0;31m'
    green = '\033[0;32m'
    ncol = '\033[0m'

    # 4. Create config file
    create_config_json(name=name, aut=aut)
    
    # 5. Create HEAD, BODY and FOOTER
    create_head_html(name = name)
    create_body_html(name, today, aut)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    footer_template_path = os.path.join(script_dir, "templates", "footer.html")
    new_footer_path = os.path.join(".labnotebook", "footer.html")
    shutil.copy(footer_template_path, new_footer_path)

    # 6. Copy style.css file
    css_template_path = os.path.join(script_dir, "templates", "style.css")
    new_css_path = os.path.join(".labnotebook", "labstyles.css")
    shutil.copy(css_template_path, new_css_path)

    # 7. Return messages
    print(f"\n{green}.labnotebook folder successfully created")
    print(f"{red}Mandatory: when updating the notebook, make sure you are in {os.getcwd()}")
    print("Never change the .labnotebook folder name or content")
    print(ncol)


def create_config_json(name, aut):
    """
    This function creates the config.json file in the .labnotebook folder
    """
    config = {"NOTEBOOK_NAME": f"{name}", 
              "LAB_AUTHOR": f"{aut}",
              "LAST_COMMIT": None,
              "LAST_DAY": None,
              "SHOW_ANALYSIS_FILES": True,
              "LAB_CSS": ".labnotebook/labstyles.css",
              "ANALYSIS_EXT": ['.html']}
    
    filename = '.labnotebook/config.json'
    with open(filename, 'w') as file:
        json.dump(config, file, indent = 4)


def create_head_html(name):
    """
    This function creates the head.html file based on the head template, by changing the title meta.
    """
    # 1. Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Define the path to the 'templates' folder relative to the script's directory
    head_template_path = os.path.join(script_dir, "templates", "head.html")

    # 3. Perform the substitution
    try:
        # 3.1 Read the content of the template file
        with open(head_template_path, "r") as template_file:
            template_content = template_file.read()

        # 3.2 Perform the substitution
        head_content = template_content.replace("{name_placeholder}", name)

        # 3.3 Define the path for the new .labnotebook/head.html file
        new_head_path = os.path.join(".labnotebook", "head.html")

        # 3.4 Write the modified content to the new file
        with open(new_head_path, "w") as new_head_file:
            new_head_file.write(head_content)

    except FileNotFoundError:
        print("Template file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def create_body_html(name, today, aut):
    """
    This function creates the body.html file based on the body template, by changing the title, the author and the date.
    """
    # 1. Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 2. Define the path to the 'templates' folder relative to the script's directory
    body_template_path = os.path.join(script_dir, "templates", "body.html")

    # 3. Perform the substitution
    try:
        # 3.1 Read the content of the template file
        with open(body_template_path, "r") as template_file:
            template_content = template_file.read()

        # 3.2 Perform the substitution
        body_content = (template_content.replace("{name_placeholder}", name).
                        replace("{today_placeholder}", today).
                        replace("{aut_placeholder}", aut))

        # 3.3 Define the path for the new .labnotebook/head.html file
        new_body_path = os.path.join(".labnotebook", "body.html")

        # 3.4 Write the modified content to the new file
        with open(new_body_path, "w") as new_body_file:
            new_body_file.write(body_content)

    except FileNotFoundError:
        print("Template file not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def update_labnotebook(force_update):
    """
    This function updates body.html and config.json files in .labonotebook folder by looping through all commits not already inclded.
    """
    # 1. Get useful variables
    red = '\033[0;31m'

    # 2. Check for .labnotebook folder and config.json files
    if not os.path.exists(".labnotebook"):
        print(f"{red}Error: There is no .labnotebook folder in the current working directory. "
              "Please go to the folder where .labnotebook is.")
        sys.exit(2)
    
    config_file = os.path.join(".labnotebook", "config.json")
    try:
        with open(config_file, "r") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print(f"{red}Error: There is no config file in .labnotebook folder. Please provide the config file.")
        sys.exit(2)
    
    # 3. Check for staged files
    git_status = subprocess.run("git status", shell=True, stdout=subprocess.PIPE, text=True)
    if "Changes to be committed:" in git_status.stdout:
        print(f"{red}Error: You have staged files to be committed. This is incompatible with updatenotebook. "
              "Please commit those changes, restore the files, or stage them prior to running this function.")
        sys.exit(1)
    
    # 4. Reset config and head if force_update
    if force_update:
        create_config_json(name = config.get('NOTEBOOK_NAME'), 
                           aut = config.get('LAB_AUTHOR'))
        with open(config_file, "r") as config_file:
            config = json.load(config_file)
        create_body_html(name = config.get('NOTEBOOK_NAME'), 
                         today = datetime.now().strftime('%Y-%m-%d'), 
                         aut = config.get('LAB_AUTHOR'))
        
    # 5. Get list of commits sha
    last_commit = config.get('LAST_COMMIT')
    sha_list = get_sha_list(last_commit)

    # 6. Remove main and body closing tags from body.html
    with open(".labnotebook/body.html", "r") as body_file:
        body_content = body_file.read()
        body_content = (body_content.replace("</main>", "").
                        replace("</body>", ""))
    
    # 7. Get info about each commit
    analysis_ext = config.get('ANALYSIS_EXT')
    excluded_patterns = get_excluded_patterns()
    commits_info = {sha: get_commit_info(sha, analysis_ext, excluded_patterns) for sha in sha_list}

    # 8. Write info into body.html and update config
    write_update_files(commits_info, body_content, config)
    

def get_sha_list(last_commit):
    """
    This functions returns a list of commits sha (from oldest to newest) that have not been already included in the notebook.
    """

    red = '\033[0;31m'
    yellow = '\033[1;33m'

    # 1. Get list of all commits
    git_sha = subprocess.run("git log --pretty=format:%h --reverse", shell=True, stdout=subprocess.PIPE, text=True).stdout.split('\n')

    # 2. Subset for new commits
    # 2.1 If git history is empty, return error
    if git_sha == ['']:
        print(f"{red}Error: Git history is empty")
        sys.exit(5)

    # 2.2 Return all if last commit is None
    if last_commit is None:
        return git_sha
    
    # 2.3 Raise error if last commit is not in git_sha list
    if last_commit not in git_sha:
        print(f"{red}Error: Last commit used for the lab notebook ({last_commit}) is not in the current git log history."
              f"\nIt is possible that you have changed commit history. Please check your git log and insert the commit SHA to use in the config file or force the update to start again from the beginning of the git history using labnotebook update -f/--force.")
        sys.exit(5)
    
    # 2.4 Perform the subset
    index = git_sha.index(last_commit)
    git_sha = git_sha[index + 1:]

    # 2.5 Interrupt if last_commit is actually the last commit in history
    if len(git_sha) == 0:
        print(f"{yellow}Warning: LAST_COMMIT is already the last commit in history. Nothing to update.")
        sys.exit(5)

    # 3. Return git_sha
    return git_sha


def get_excluded_patterns():
    """
    This functions returns a list of the patterns to exclude in analysis files.
    """
    try:
        with open('.labignore', 'r') as f:
            excluded_patterns = f.read().splitlines()
            excluded_patterns = [pattern.replace('*', '.*') for pattern in excluded_patterns]
    except FileNotFoundError:
        excluded_patterns = []
    finally:
        return excluded_patterns



def get_commit_info(commit_sha, analysis_ext, excluded_patterns):
    """
    This function returns a dictionary of the information about the commit specified in commit_sha. These info are: date, author, title, message and changed files.
    """
    date, author, title = subprocess.check_output(['git', 'log', '-n', '1', '--pretty=format:%cs%n%an%n%s', commit_sha], text=True).strip().split('\n')
    message = subprocess.check_output(['git', 'log', '-n', '1', '--pretty=format:%b', commit_sha], text=True).strip()
    changed_files = subprocess.check_output(['git', 'show', '--pretty=%n', '--name-status', commit_sha], text=True).strip().split('\n')
    changed_files = {file.split('\t')[1] : file.split('\t')[0] for file in changed_files}
    analysis_files = [key for key,_ in changed_files.items() if any(ext in key for ext in analysis_ext) and not any([re.search(pattern, key) for pattern in excluded_patterns])]
    commit_info = {'date': date,
                   'author': author,
                   'title': title,
                   'message': message,
                   'changed_files': changed_files,
                   'analysis_files': analysis_files}
    return commit_info


def write_update_files(commits_info, body_content, config):
    """
    This function writes the commit elements into body.html and updates the config.json file.
    """
    # 1. Loop through commits
    for sha, commit in commits_info.items():
        # 1.1 Check last day
        if config.get('LAST_DAY') != commit.get('date'):
                body_content += f"<h2 class='day-el'>{commit.get('date')}</h2>\n\n"
                config['LAST_DAY'] = commit.get('date')
        
        # 1.2 Write commit div
        body_content += f"<div class='commit-el' id='{sha}'>\n"
        body_content += f"<h3 class='title-el'>{commit.get('title')}</h3>\n"
        if commit.get('message') == '':
            pass
        else:
            body_content += f"<p class='mess-el'>{commit.get('message')}</p>\n"
        body_content += f"<p class='author-el'>Author: {commit.get('author')}</p>\n"
        body_content += f"<p class='sha-el'>sha: {sha}</p>\n"
        if len(commit.get('analysis_files')) == 0:
            body_content += "<div class='analyses-el'>Analysis file/s: <code>none</code></div>\n"
        else:
            body_content += f"<div class='analyses-el'>Analysis file/s:\n<ul class='analysis_list'>\n"
            for a_file in commit.get('analysis_files'):
                body_content += f"<li><code><a href='{a_file}' target='_blank'>{a_file}</a></code></li>\n"
            body_content += "</ul>\n</div>\n"
        body_content += "<details>\n<summary>Changed files</summary>\n<ul class='changed_list'>\n"
        for c_file in commit.get('changed_files'):
            body_content += f"<li>{c_file}</li>\n"
        body_content += "</ul>\n</details>\n</div>\n"

        # 1.3 Update last commit
        config['LAST_COMMIT'] = f"{sha}"

    # 2. Insert closing tags
    body_content += "</main>\n</body>"

    # 3. Write body.html
    with open('.labnotebook/body.html', "w") as new_body_file:
            new_body_file.write(body_content)

    # 4. Write config.json
    with open(".labnotebook/config.json", 'w') as file:
        json.dump(config, file, indent = 4)


def export_labnotebook(output_file, force, link):
    """
    This function exports the labnotebook into a single (or multiple) html file ready to read.
    """
    # 1. Get useful variables
    red = '\033[0;31m'

    # 2. Check for .labnotebook folder, config.json and .html files
    if not os.path.exists(".labnotebook"):
        print(f"{red}Error: There is no .labnotebook folder in the current working directory. "
              "Please go to the folder where .labnotebook is.")
        sys.exit(2)
    
    config_file = os.path.join(".labnotebook", "config.json")
    try:
        with open(config_file, "r") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        print(f"{red}Error: There is no config file in .labnotebook folder. Please provide the config file.")
        sys.exit(2)

    required_files = [
    '.labnotebook/head.html', 
    '.labnotebook/body.html', 
    '.labnotebook/footer.html', 
    config.get('LAB_CSS')
    ]

    for file in required_files:
        if not os.path.exists(file):
            print(f"Error: There is no {file} file.")
            sys.exit(2)
    
    # 3. Check if file already exists and force is False
    if os.path.exists(output_file) and not force:
        print(f"{red}Error: {output_file} already exists. Use -f/--force to overwrite it.")
        sys.exit(1)
    
    # 4. Read head.html and edit it
    with open('.labnotebook/head.html', 'r') as head_file:
        output_content = head_file.read()
    output_content = output_content.replace("</head>", "")
    if link:
        output_content += f"<link rel='stylesheet' href='{config.get('LAB_CSS')}'>\n"
    else:
        with open(config.get('LAB_CSS'), 'r') as style_file:
            output_content += f"<style>\n{style_file.read()}\n</style>\n"
    
    if not config.get('SHOW_ANALYSIS_FILES'):
        output_content += "<style>\n.analyses-el {display: none;}\n</style>\n"

    output_content += "</head>\n"
    
    # 5. Read body.html and insert into output content
    with open('.labnotebook/body.html', 'r') as body_file:
        output_content += f"{body_file.read()}\n"
    
    # 5. Read footer.html and insert into output content
    with open('.labnotebook/footer.html', 'r') as footer_file:
        output_content += f"{footer_file.read()}\n"

    # 6. Write output file
    with open(output_file, 'w') as output_file:
        output_file.write(output_content)

    
def main():
    parser = argparse.ArgumentParser(description="Lab Notebook Tool")
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__, help="Show package version")

    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create a new lab notebook")
    create_parser.add_argument("-n", "--name", required=True, help="Name of the lab notebook. If the name should contain more words, wrap them into quotes")

    update_parser = subparsers.add_parser("update", help="Update lab notebook")
    update_parser.add_argument("-f", "--force", help="Force the update", default=False, action="store_true")

    export_parser = subparsers.add_parser("export", help="Export lab notebook to an html file")
    export_parser.add_argument("-o", "--output", required=True, help="Path/name of the output HTML file")
    export_parser.add_argument("-f", "--force", help="Force the overwriting of the output file if already present", default=False, action="store_true")
    export_parser.add_argument("-l", "--link", help="Link style file in head. By default style file is copied in <style></style> tags in head", default=False, action="store_true")

    args = parser.parse_args()

    if args.command == "create":
        if not args.name:
            create_parser.error("-n/--name is required for the 'create' command. Please provide the name of the notebook.")
        create_labnotebook(args.name)
    elif args.command == "update":
        update_labnotebook(args.force)
    elif args.command == "export":
        if not args.output:
            export_parser.error("-o/--output is required for the 'export' command. Please provide the name of the output file.")
        export_labnotebook(args.output, args.force, args.link)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
