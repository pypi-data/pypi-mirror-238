<h1 align="center">Startnewproject 🖥🗂️</h1>

This package includes a function to create a new project folderm with the desired tree, git and pylabnotebook initialized.

**DEPENDENCY**: this tool depends on git and <a href="https://github.com/mmiots9/pylabnotebook" target="_blank">pylabnotebook</a>. Please install git and configure it prior to using this package.

<h3 style="margin-bottom:3px;">Features</h3>
<ul>
  <li>Automatically create folder tree based on the configuration file</li>
  <li>Customizable configuration file</li>
  <li>Pre-compiled README in each folder, with the desired format (.txt, .md, or .html)</li>
  <li>Git initialization, with .gitignore and .gitattributes as well</li>
  <li>pylabnotebook initialization</li>
</ul>

<h3>Installation</h3>
To install the package, run:

```
pip install startnewproject
```

This will install the startnewproject package, as weel as its dependency; you can then run <code>startnewproject</code> function from within the terminal (detailed explanation below).

<h3>Start a new project</h3>
To start a new project, just run

```
startnewproject -n name_of_the_project
```

If you want to have spaces in your name, just wrap it into quotes. If the folder already exists, an error will be returned; use <code>-f/--force</code> to overwrite the existing folder.
A folder is created with the default tree structure.

<h3>Costumize configuration</h3>
To use a costumize tree structure, you have to provide a configuration file structured like the one in <code>templates/config.json</code> as input with the <code>-c/--config</code> flag.<br>
It must be a .json file containing as keys: "description" (a string, can be empty), "subfolders" (a dictionary of subfolders. Check the template to see an example), "files" (a list of file names, can be empty), ".gitignore" (a list of patterns to include in .gitignore), ".gitattributes" (a dictionary of things to include in .gitattributes. Check the template for an example).

<h3>Issue reporting and suggestions</h3>
If you find any issue or you want to suggest some edit, please feel free to open an issue or a pull request.
