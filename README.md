# WIP VFX_ProdTracker
Production tracking tool for VFX projects, supporting multiple users

## Requirements Document:

This is going to be a short documents outlining the requirements for this project. 

### Scope:
The aim of the project is to produce a basic production tracking tool. First and foremost, it should aid users in managing and tracking their shot work in a website like manner. 
Hence, the project can be broken down into two main stages:
 - Stage 1: Standalone web-based production tracker, which can offer its basic functionality, but on a manual update basis. 
 - Stage 2: Full integration with the DCC tools, using TIK manager. This will allow for the web-app to directly work with the user's DCC and merge tracking directly with their work

MVP is defined as a complete Stage 1.  

### Users:
This project is aimed at small teams and individuals, working on CGI/film related products, that will benefit from shot-by-shot tracking. 

### Requirements and functions:
    Core functionality: 
        The web app must give the user tools to track their project, which means:
        1. Project creation/deletion cycle [x]
        2. Specifying the metadata for the project, such as name, type, status, number of shots, etc []
        3. Populating the project page (unique for each project) with said metadata and enabling it for editing by the user []
        4. Manual editing of the shots and project status by the user. []

    Extended functionality:
        This functions are expansions of the core, aimed to give the project bigger scope of use:
        1. User login/sign up system
        2. Storing only projects relevant for the user in the user's account 
        3. Enabling sharing of the project by users between multiple users 
        4. User permissions inside the project

    Post MVP nice-to-have's functionality:
        This functions are quality of life improvement for the base application:
        1. Better UI
        2. Comment on each shot/asset/version
        3. Individual version publishing with playblasts/thumbnails

### Tech stack:
    Node.js
    Vite
    React/Javascript
    Tailwindcss
    Flask/Python
    SQLite

