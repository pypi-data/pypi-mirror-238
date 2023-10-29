<h1 align="center">Labnotebook 📔🖥</h1>

This project aims to help bioinformaticians in creating the so called "Laboratory notebook" automatically, thanks to git workflow manager.

**IMPORTANT**: this tool is based on git and its application, in particular, through git history it will create an html notebook divided by date and commit.

<h3 style="margin-bottom:3px;">Features</h3>
<ul>
  <li>Automatically create a laboratory notebook</li>
  <li>Customizable CSS file</li>
  <li>Direct link to analysis files (expecially for user who creates .html reports. e.g. markdown or jupyter notebook html)</li>
  <li>Export to html</li>
</ul>

<h3>Installation</h3>
To install the package, run:

```
pip install pylabnotebook
```

This will install the pylabnotebook package; you can then run <code>labnotebook</code> function from within the terminal (detailed explanation below).

<h3>Notebook structure</h3>
The structure of the notebook is very simple. You can see an example <a href='https://miotsdata.netlify.app/it/bash/mie_funzioni/example.html' target='_blank'>here</a>.

<p style="margin-bottom:0px;">On top, you have the notebook name, the author and the notebook creation date. Then, for each day, you have a list of all the commits done, organized as follow:</p>
<ul>
  <li>Commit message (first line)</li>
  <li>Commit body</li>
  <li>Commit author</li>
  <li>Commit sha</li>
  <li>Analysis file (which can be hidden if you don't have this type of features)</li>
  <li>List of changed files</li>
</ul>

<h3>Create a notebook</h3>
To create a notebook, go to the folder in which is present the .git folder and type <code>notebook create -n &#60;name_of_the_notebook&#62;</code>. If you want to have spaces in your name, just wrap it into quotes.

A .labnotebook folder is created, containing config.json file, a basic .css file and three file containing head, body and footer html file.

**IMPORTANT**: never change the name of the created folder and its files!

<h3>Update a notebook</h3>
When you want to update the notebook, go to the folder in which is present the .git folder, type <code>notebook update</code>. It will check for new commits and upate the files in .labnotebook folder.
<br>
If the git history have changed and the last commit present in the labnotebook is no longer in git history, it will raise an error; you can skip this by forcing the update (<code>-f/--force</code>).

**IMPORTANT**: After each notebook update a commit is made with labnotebook as author. This will ensure that these commits are not considered during the update, as only commits without labnotebook as author are used.

<h4>Link to analysis files</h4>
When updating the notebook, it automatically create a list of analysis files for each commit with direct links to them. By default, it takes all the .html files changed/added in that commit.<br>
If you want to add different extensions, you can update the .labnotebook config.json file by adding/removing extensions in the ANALYSIS_EXT variable. Each extension should be separated by a comma, as it is considered an array (eg. "ANALYSIS_EXT": ['.html', '.txt'])Just type the extension, not wildcards or other special characters.<br>
Moreover, by creating a ".labignore" file, you can exclude some files/folders to be recognized as analysis files (as for a standard .gitignore file it will use wildcards).

<h3>Export html file</h3>
When you want to export the full html file containing the notebook, go to the folder in which is present the .git folder, type <code>labnotebook export -o &#60;name_of_the_output_file&#62;</code>.

<h3>Issue reporting and suggestions</h3>
If you find any issue or you want to suggest some edit, please feel free to open an issue or a pull request.
