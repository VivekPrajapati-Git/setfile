Setfile : An AI Based File organizer

Suppose if you have clusters of file and you are bored organizing it. Here's the solution

Introducing Setfile, where you can organize your files with one single command. This tool is available in both CLI and Well as GUI

Following are the steps to setup your project:

1. clone the repository

2. Run this command - npm install -r requirements.txt

3. Create a secret folder

4. Create a goolge api key and enable GMail API

5. Following are the command that you can run as cli command: 

        cd src/setfile/

        python -m setfile organize --path "folder path"

        python -m setfile revert

        python -m setfile gmail-auth

        python -m setfile download

6. for running GUI

        cd GUI

        python main.py