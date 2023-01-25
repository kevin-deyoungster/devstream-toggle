## Background 
Whenever I wanted to stream on Twitch, I had to undock personal apps and dock only the apps I needed for my dev stream. I did it manually enough times to realise that it required automating. I created this Alfred workflow which runs a python script to handle switching to and from 'dev stream' mode.


## Devstream-toggle
Automation script to replace MacOS dock with a desired list of apps (as specified in config), and change audio output 

<img width="639" alt="Screenshot 2023-01-24 at 23 40 49@2x" src="https://user-images.githubusercontent.com/24400570/214506719-ca5e4294-1b8f-475e-8aa3-c3189048a410.png">

## Pre-requisites 
1. Install:
    - [Alfred 5](http://alfredapp.com) - application launcher
    - [dockutil](https://github.com/kcrawford/dockutil) - does the heavy lifting of modifying the MacOS dock
    - [switchaudio-osx](https://github.com/deweller/switchaudio-osx) - for changing audio output source 

2. Create your own onfig.json file and replace the `CONFIG_FILE` variable in the python script 

3. Update your Alfred workflow with the updated python script after (2)

## Alfred Workflow 
<img width="919" alt="Screenshot 2023-01-24 at 23 47 20@2x" src="https://user-images.githubusercontent.com/24400570/214507815-558c274d-db54-4b34-9608-81b2e1dcd81b.png">

