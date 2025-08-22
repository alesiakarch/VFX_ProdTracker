# Tracktor VFX
Production tracking tool for VFX projects, supporting multiple users

## Supporting Documents:

A Requierment Document and a Design Document are available at the root of the repo.

## Installation:

### Prerequisites:

Podman is requiered at this state to self-host the web app.

TIK Manager must be installed to use Tracktor plugin for TIK.

### Linux

0. Ensure you have podman and podman-compose installed
1. Download and extract the source code
2. Navigate to the VFX_prodtracker directory in terminal (this directory will have docker-compose.yml in it)
3. Run podman-compose up --build
4. Wait until the build is done. If prompted to select an image, select: docker.io/vfx_prodtracker-main...
5. Once the backend and front end are build and running, navigate to localhost:5173

Frontend: localhost:5173
Backend: localhost:8080/api/users (valid url, check out the rest in the endpoints)

### Windows

0. Ensure you have podman and podman-compose installed
1. Download and extract the source code
2. Navigate to the VFX_prodtracker directory in terminal (this directory will have docker-compose.yml in it)
3. Activate podman on windows with: podman machine start
4. Run podman-compose up --build
5. Wait until the build is done. If prompted to select an image, select: docker.io/vfx_prodtracker-main...
6. Once the backend and front end are build and running, navigate to localhost:5173

### TIK plugin

0. Ensure you have TIK manager installed - so far tested in Maya and Houdini only, but may be available in other DCCs.
00. Note the tik_manager4/ installation directory
1. Have a working build of Tracktors backend
2. Download the tik_tracktor filed from source code
3. Run ./installer.py from the terminal from tik_tracktor folder. Installed will prompt for a tik installation path, if it isn't a default windows one, and then copy the files where they are supposed to be.
4. Open the DCC package and check for the Tracktor menu.
5. Free to use!


### Tech stack:

    Node.js
    Vite
    React/Javascript
    Tailwindcss
    Flask/Python
    SQLite


