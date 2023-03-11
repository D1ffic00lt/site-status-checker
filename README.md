<h1 align="center">Site Status Checker</h1>
<h2 align="center">Console application for monitoring the status of sites from a .csv file</h2>

## Task
> 123

## Implementation
> 123

## Structure
- checker
- - units 
- - - &#95;&#95;init&#95;&#95;.py
- - - controller.py
- - - exceptions.py
- - - reader.py
- - &#95;&#95;init&#95;&#95;.py
- - config.py
- - display.py
- - sitestatuschecker.py 
- app.py
- Dockerfile
- run.sh
- requirements.txt
- .dockerignore 
- .gitignore
- README.md 
- LICENCE.md

## Files and directories

| Name                                                       | Description                                                                                                                                           |
|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| [checker](checker)                                         | All main program code                                                                                                                                 |
| [checker/units](checker/units)                             | Custom errors, handlers and csv file readers                                                                                                          |
| [checker/units/controller.py](checker/units/controller.py) | Single site request handler                                                                                                                           |
| [checker/units/exceptions.py](checker/units/exceptions.py) | Custom errors                                                                                                                                         |
| [checker/&#95;&#95;init&#95;&#95;.py](checker/__init__.py) | Main project initialization file                                                                                                                      |
| [checker/config.py](checker/config.py)                     | Application configuration (regular expressions, log formats, etc.)                                                                                    |
| [checker/display.py](checker/display.py)                   | Web part of the application, responsible for outputting data to the console                                                                           |
| [app.py](app.py)                                           | Code (in some cases an example) that performs the function of deploying an application                                                                |
| [requirements.txt](requirements.txt)                       | Libraries required to use the application                                                                                                             |
| [Dockerfile](Dockerfile)                                   | Docker application image                                                                                                                              |
| [run.sh](run.sh)                                           | a bash script that deploys and executes a docker container if docker is available (otherwise, the library is installed and the app.py starts working) |

