# 1. Introduction and Overview  

Tracktor is a web-based VFX production tracking application designed for freelancers, students, and small-sized creative teams. This project was conceived to bridge the gap between professional production tracking tools and the lightweight needs of individuals or small teams. It takes inspiration from established pipeline practices while remaining accessible, open-source, and easy to deploy on personal or shared machines.  

While larger studios often rely on commercial solutions like ShotGrid or Kitsu, Tracktor aims to offer a simplified, accessible, and opensource alternative that can be deployed locally or online. Its modular design allows future integration with external tools such as TIK Manager, enabling deeper DCC (Digital Content Creation) integration for asset publishing and version control.

The purpose of this document is to outline the technical and structural design of this project and provide a plan for its development.

This has to be noted: the project is also being developed as a Master's thesis, and hence requires a specifically defined MVP for the aforementioned thesis submission, which might or might not include the set out general goals for the project.

This document serves as a reference for:  

- Developers contributing to the frontend, backend, or integration components.  

- Supervisors and instructors reviewing the system for academic or production purposes.  

- Contributors interested in extending the application or integrating it with their own pipelines.

Further in this section we will go over the goals and non-goals of Tracktor, as well as project scope, primary features and give a quick overview of the rest of the document.

# 1.1 Goals and Non-goals

## Goals

Tracktor is designed to offer a simplified yet functional pipeline tracker. The following are the core goals:

- Support user accounts, enabling personalized and team-based project access

- Provide tools for project creation, including management of shots and assets

- Enable status tracking across departmental tasks

- Allow notes to be attached to shots and assets for team collaboration

This is where the web-app thesis MVP is defined. Further features will be moved into a roadmap, which does not necessary match the Master thesis submission schedule.

## Primary features

To meet the above goals, Tracktor includes the following features:

- User registration and login system

- Project dashboard with the ability to create, delete, and view projects

- UI with functionality to add/edit shots and assets within a project

- Status buttons or dropdowns for task departments (MOD, RIG, etc.)

- Notes fields or modal dialogs for assets/shots

## Non-Goals

At this development stage, Tracktor intentionally does not address the following:

- Built-in file storage or media review functionality

- In-app file uploads or rendering previews

- Permission hierarchies beyond simple ownership

These are considered out of scope for the MVP but may be included in a future roadmap.  

# 1.2 Key requiements and objectives

For project requiements and objectives please refer to the requiements document in the project repository's README

Summary of the requiements document:

1. Core Requirements

These are the essential features the app must support to be usable for production tracking:  

- Users must be able to create and delete projects.  

- Users must be able to define and edit project metadata (name, type, status, number of shots, etc).

- Each project must have a unique, editable project page that displays relevant information.

- Users must be able to manually update the status of projects and individual shots.

2. Extended Requirements (Post-Core Scope)

These expand usability and collaborative functionality:

- A user authentication system (sign up, log in, log out).

- Projects should be linked to specific user accounts.

- Projects should be shareable between users.

- Each project should support user roles/permissions (e.g., admin, contributor, viewer).  

3. Post-MVP / Nice-to-Have Features

- Improved UI and layout (responsive, styled with Tailwind or similar).

- Comments/notes system for shots, assets, or versions.

- Support for uploading visual media (thumbnails, playblasts) linked to version entries.  

# 1.3 Brief description of the software system

Tracktor is envisioned to be a web-based standalone app, with potential for DCC intergration as a plugin.

For the standalone app functionality, this is the basic stack:

- The frontend is developed using React, providing an interactive user interface.

- The backend is powered by Flask (Python), which handles user authentication, data processing, and routing.

- Data is stored in an SQLite database, accessed through backend API endpoints.  

## TIK Manager plugin

As mentioned above, Tracktor can have potential as an integrated trackign plugin that can connect to the DCC of choice and allow users to sync their work directly. To demonstrate such ability and potential, the second part of the thesis involves developing a Tracktor plugin for TIK manager - an opensource pipeline tool, that handles projects systems and version control on local machines. TIK manager has gained popularity in the CGI community, and while it doesnt provide production tracking capabilities directly, it has integration with other commercial tracking software like Autodesk Flow (previously known as Shotgrid) and Kitsu. The goal of the project here is to create a Tracktor plugin that mirrors the Shotgrid/Kitsu plugins functionality (as an MVP) and can demonstrate Tracktor as a viable pipeline tracker option.

TIK plugin goals and requerments:

- A Python client-base plugin that will make calls to the Tracktor API

- A functionality to log in into Tracktor from TIK

- An ability to pull projects from Tracktor to TIK

- Syncing functionality between Tracktor and TIK


# 1.4 Document overview

The rest of this design document includes infromation on system archinecture, providing a high-lever overview of the systems and how the set goals are going to be acheved. The section after this will be dedicated to Data design, looking into the database structure and flow of data within the project. Then Component design section will go into greater detail into the individual modules, defined in the system architecture. After this, the Interface design section will discuss how the app interacts within itself and external tools like TIK manager. The following UI section is about the decisions regarding the user-facing visuals and user expereince and expectations when interacting with the main website. Deployment strategies will be discussed in the following section, outlining how the project is meant to be accessed and distributed. Any knowledge of technical debt or external requierments will be outlined in the Assumptions and Dependancies, and Future work will talk about possible improvements after the Master thesis submission.

# 2. System Architecture

# 2.1 High-lever overview

The architecture of Tracktor is based on a modular full-stack design that separates concerns between the frontend user interface, backend logic, and persistent storage. Each component communicates through a defined set of RESTful API endpoints, ensuring a clean separation and scalability. A diagram of this architecture can be found below:

![A high-level diagram of the architecture](https://livebournemouthac-my.sharepoint.com/:i:/g/personal/s5221034_bournemouth_ac_uk/Eb3ZtlErxtNMj5KmGlGr1yUBFl7w8dtSCYDoe2L_L9EORw?e=hK4XQ1)

# 2.2 Component descriptions

The system consists of several core components, each responsible for a distinct layer of functionality:

## Frontend (React with Tailwind CSS & Headless UI)

The frontend is a single-page application (SPA) developed using React. It provides the user interface and handles all user interactions. Tailwind CSS and Headless UI are used to implement a responsive and accessible UI design. React components are organized into reusable modules (e.g., buttons, forms, layouts).

## Backend (Flask)

The backend is built with the Flask web framework in Python. It handles the storing logic, routes API requests, and communicates with the database. Each major data entity (e.g., user, project, shot, asset) is represented as a separate Python module or class for modularity.  

## API (RESTful Endpoints)

The frontend and backend communicate via RESTful HTTP endpoints defined in backend/main.py. These routes allow clients to perform standard operations such as GET (read), POST (create), PUT (update), and DELETE on application data.

## Database (SQLite, with potential migration to PostgreSQL)

The application uses a relational database to persist user and project data. The schema currently includes tables for Users, Projects, Shots, and Assets. SQLite is used during development for simplicity, with future potential to migrate to PostgreSQL for scalability.

## Testing (Flask Backend Unit Tests)

The backend includes unit and integration tests to validate API behavior and ensure reliability. These tests cover data validation, route logic, and error handling.  

## TIK Manager Plugin

TIK plugin also consists of the following:  

- Python based client wrapper for making calles to the API

- PyQt based shelf UI

# 2.3 Design patterns and architectural styles

The Tracktor system follows a client-server architecture, where the frontend React application acts as the client, and the Flask backend serves as the server exposing RESTful APIs. This clear separation enables independent development, testing, and deployment of the frontend and backend components.

##  RESTful API Design:

The backend exposes RESTful endpoints to allow standardised communication between the client (React UI), the TIK plugin (Python client), and the backend services. 

## Layered Architecture:

The system is divided into distinct layers — presentation (React UI), application logic (Flask routes and business logic classes), and data persistence (SQLite/PostgreSQL). This separation improves maintainability and testability.

## Design Patterns:  

Model-View-Controller (MVC) Inspired: Although Flask does not enforce MVC strictly, the backend organizes code into models (database classes), views (Flask route handlers), and controllers (entity logic inside class methods).

Repository Pattern: Database access is encapsulated within model classes to isolate data logic from the rest of the application.

For TIK Manager plugin - Client Wrapper Pattern: The TIK plugin acts as a client wrapper that encapsulates all communication with the backend API, simplifying plugin UI code and allowing easy changes in API endpoints or authentication methods without affecting UI components.

# 2.4 Discussion of important design decisions and trade-offs

 ### SQLite vs PostgreSQL:

SQLite was selected for initial development due to its simplicity, zero-configuration setup, and ease of use. However, it has limitations in concurrency and scalability. PostgreSQL is considered for future deployment to handle larger datasets, concurrent users, and production robustness. This staged approach reduces complexity during early development but requires future migration planning.

### Flask Framework Choice:

Flask was chosen because of its lightweight and flexible nature, which aligns well with the scope of the Tracktor project and developer familiarity. The trade-off is that Flask requires more manual setup and lacks built-in features compared to full-stack frameworks like Django, but this also provides more control and customization.

### React with Tailwind and Headless UI:

React enables building a modern and responsive user interface with reusable components. Tailwind CSS provides a utility-first styling approach for fast UI development, while Headless UI components offer accessible interactive elements. This combination accelerates UI development but introduces a learning curve and larger frontend dependencies.

### Plugin Communication via REST API:

The TIK plugin is implemented as a Python client that interacts with the backend through RESTful requests. This approach allows plugin UI code to remain lightweight and rely on the existing backend logic, reducing code duplication. The trade-off includes potential latency and network dependency, but the modularity and maintainability benefits outweigh these drawbacks.

# 3. Data Design

The data design defines how Tracktor stores, organizes, and retrieves data across its main entities such as users, projects, shots, and assets. The system uses an SQLite database during development, with potential migration to PostgreSQL for production scalability.

# 3.1 Database Structure and Table Layouts


[TracktorDB Diagram](https://livebournemouthac-my.sharepoint.com/:i:/g/personal/s5221034_bournemouth_ac_uk/EU_CnkkuEohFtlSuWMU9AEYB_Z6nbLBC9A6O9TTM79oocw?e=PpesS4)


# 3.2 Data Flow and Storage

### Frontend to Backend Flow:

Users interact with the React frontend, which sends POST, GET, PATCH, and DELETE requests to the Flask API. The backend handles these requests, validates input, and performs database operations.
  

### Backend to Database Flow:

The Flask backend interacts with SQLite using sqlite3 queries (or ORM if later switched). It maps the API requests to SQL commands and handles formatting data for API responses.

### TIK Plugin Communication:

The Python plugin sends HTTP requests to the Flask backend, just like the frontend. For example, a “Create Project” button in the plugin sends a POST request with project data, which the backend stores in the Projects table.

# 3.3 Data Validation and Integrity

Validation Rules for Tracktor to work properly:

- Usernames must be unique and non-empty.  

- Passwords must be hashed before storage.

- Projects must have unique names per user.  (ADD THIS)

- Shot and asset names are validated against duplicates within a project. (ADD THIS)

Database Integrity:

- Foreign keys (e.g., owner_id, project_id) are enforced to maintain relationships.

- Cascading deletes may be added to remove associated shots/assets when a project is deleted. No hanging db entries

# 3.4 Retrieval Patterns

Projects for a specific user are retrieved by joining Projects and UserProjects using the user_id.  
Shots and assets are retrieved based on their project_id, with optional filtering by department status.
All data passed to the frontend or plugin is formatted as JSON via Flask responses.

# 4. Component Design

The component design section provides detailed information about individual modules or components within the system. This includes their specific functionality, what inputs they need and outputs they produce, and any algorithms or data structures they use.

This section will present a summary of the individual components structure and how they work.

# 4.1 Frontend Components (React)

## Purpose and Responsibilities

The Purpose of Tracktor's Frontend is to provides the user with the interface for the apps functionality. It enables access to Tracktor's backend in the readable and convienient way. Additionally, the frontend captures the user input and interacts with the backend via the API calls. One of the main features is also to render any data updates dynamically (by using useState and useEffect), to keep the pages the users see up to date as much as possible.  

### Key Components

The frontend is modular and consists of the following:

- main.jsx: Initialises the App.jsx

-  <App.jsx />: Main application wrapper, manages routing between pages.

The rest of the components are stored in either pages/ or components/, depending on the funtion.

Pages contain only Javascript files, that compile to a webpage, like:  

-  <LandingPage.jsx />: Displays user's projects and “Create Project” button.

-  <CreateProjectPage.jsx />: Contains input forms for creating new projects.

-  <ProjectPage.jsx />: Displays a specific project’s metadata, shots, and assets.

-  <Join_project_page.jsx />: Displays the field and notification for the user to put the share code in and connect it to its LandingPage

-  <Share_project_page.jsx />: Displays the project share code and a button to generate it.

-  <Item_page.jsx />: Displays the versions and metadata of a specific shot/asset

-  <Notes_page.jsx />: Displays all the notes and note-taking functionality of a specific item

-  <Create_asset_page.jsx />: Displays input forms for creating a new asset.

- <LoginPage.jsx/>: Displays the login/signup functionality and forms.

Components directory contains the reusable UI components, which so far are:

-  <Button.jsx  />

-  <Textbox.jsx />

-  <Navbar.jsx />

-  <StatusListbox.jsx />

-  <Table.jsx  />

## Input and Output specification

Input: User actions (clicks, form submissions).

Output: API requests, dynamic UI updates.

# Logic and Flow

Tracktor Components and Pages build together an interactive webapp, that the user can navigate.

Where data manipulation in requiered, axios is used to communicate with backed, like when pulling or creating projecs, users, assets, etc. 

Use of state and effect in React also allows for timely update of the fields and pages.

![React Components Graph](https://livebournemouthac-my.sharepoint.com/:i:/g/personal/s5221034_bournemouth_ac_uk/ETB6w9D5Us9Gg3kUoVRKQtQBjIOq-yNDa5X898o3MB2nxQ?e=55YLNC)  

## Dependencies

Tracktor's frontend is a Javascript app, which uses React library for building UI components. To assist with the components styling, Tracktor also uses TailwindCSS and some of the components (like < StatusListbox />) are based on Headless UI.

To accomodate API calls, Tracktor also relies on Axios and a Flask-based Python backend for API endpoints.


# 4.2 Backend Components (Flask)

## Purpose and Responsibilities

The backend serves as the logic layer of the application. It is also modular and consists of the main.py RESTful API file, that handles all of the calls and request logic and can be reused by different cliends, like the frontend React app, or the Python client for the TIK plugin. Complementary to the API is a set of Python classes, where each class file defines the table in the SQLite database with its methods and functionality.

Main Files:

- main.py: Entry point for API, defines all @app.route() endpoints.

- users.py, projects.py, shots.py, assets.py: Logic modules for interacting with database tables.

# Input and Output specification

Input: HTTP requests (e.g., GET, POST).

Output: JSON responses with success/error messages or data.

# Logic and Flow

The API recieved a call from the cliend, then parse and validate incoming data. If the call matches the endpoint, the funtion of the endpoint is executes, which most of the time means calling helper functions or database queries. Once the endpoint funtion is completer, the API returns formatted JSON responses for the client to work with.

[Backend Components Graph](https://livebournemouthac-my.sharepoint.com/:i:/g/personal/s5221034_bournemouth_ac_uk/Ec1k3p60I_ZEgw1GwCbghcAB1NoW25_DRA_pAuceYZVCTg?e=3SeL3P)

## Dependencies

Backend for Tracktor is based on Python Flask library and assisted by sqlite3 and JSON libraries for handling data (database and formatting).

There is potential for moving on from SQLite to PostgreSQL or other more robust databased, which will require only a change in table classes and not the backend API itself and can be done non-destructively.

# 4.3 Database

## Purpose and responsibility

The purpose of the Tracktor database is to store persistent data such as users, projects, shots, and assets. It is structured as a normalized relational database, using foreign keys for each table.

![Tracktor DB Diagram](https://livebournemouthac-my.sharepoint.com/:i:/r/personal/s5221034_bournemouth_ac_uk/Documents/MSc%20_CAVE/Masters%20Project/Screenshot%202025-08-02%20175901.png?csf=1&web=1&e=Uf5Uk5)

Tables: Users, Projects, Shots, Assets, UserProjects (for many-to-many user/project).  

## Input and Output
Input: user's calles on methods altering the database

Output: normalised tables in a database, available for data retrieval

## Logic and Flow

The database is accessed via sqlite3 in backend functions. Any interation or alterations are made through there as well. The client must send a request to have access to the database data.

Queries written manually (not using ORM).

## Dependancies

The database is of SQLite flavour of SQL, and requiers the relevant class methods to be interacted with.

# 4.4 TIK Plugin (Python Extension)

## Purpose and Responsibilities

More practival role for the Trackor plugin for TIK can be the demonstration of Tracktor's functionality in a pipeline environment.

This way the plugin will act as an external client that syncs TIK data with Tracktor backend. Such approach allows artists to connect to their Tracktor account and view/create projects from within TIK.

The plugin is copying the structure of existing production trackers such as Shotgrid and Kitsu. This means, the files for the Tracktor plugin are designed to be places in the tik_directory/management/ folder for TIK to pick it up, and any externally used libraries are destined to tik_directory/external. At the moment Tracktor plugin doesn't use any third-party libraries, which are unavailable in TIK itself, so management direcory will suffice.

The structure of the plugin is as follows:

- ui_tracktor.py: UI for TIK menu tab with buttons functionalities.

- tracktor_client.py: A Python wrapper responsible for sending/receiving HTTP requests to the Tracktor API.
  
# Input and Output specification

Input: User clicking buttons and inputing data in TIK tab.

Output: JSON data fetched from or pushed to Tracktor backend.

# Logic and Flow

In this setup the Tracktor plugin for TIK serves as a Python client for the Tracktor API. This means the interaction with the API is very similar to how React Frontend does it, apart from the plugin's UI being the client in this case.

Button click → function call → HTTP request → receive response → update UI or alert user.

![TIK Plugin Components Graph](https://livebournemouthac-my.sharepoint.com/:i:/g/personal/s5221034_bournemouth_ac_uk/EaxDulLigg1Gnvn14bozNYAB1pEComJ2aPbHHA9UnF0WwA?e=fZjHpr)

## Dependencies

For now the plugin relies on PySide2 (for UI), however this isn't a preinstalled library in the source code for the plugin, because the environment where its designed to run (Maya) is natively running on PySide2, so the installation to the project is not nessessary.

In addition, the plugin is using TIK’s ExtensionCore and TIK.Qt and Tracktor's Flask API as the endpoint.

# 5. Interface Design

The interface design section describes how different parts of the system will communicate with each other and interact with external systems or services. This includes both internal interfaces between modules and external APIs or integration points.

# 5.1 API Specifications and Protocols

The system uses a RESTful API served by the Flask backend. The frontend communicates with the backend using Axios to send HTTP requests. All data is transmitted over HTTP using JSON as the data exchange format.

Here is the list of endpoints and what they do:


-   GET /init — Initializes all database tables (users, projects, shots, assets).
    
-   GET /api/ping — Returns a simple confirmation that Tracktor API is reachable. (TIK plugin)
    
-   GET /api/users — Retrieves a list of all users (no passwords).
    
-   POST /api/users — Creates a new user with hashed password.
    
-   POST /api/login— Verifies user credentials and returns login status.
 
-  GET /api/projects — Returns all existing projects.
    
-   POST /api/projects — Creates a new project and assigns the user as Admin.
    
-   GET /api/projects/<project_id> — Returns details of a specific project.
    
-   DELETE /api/projects/<project_id> — Deletes a specific project and its shots.
   
-   GET /api/shots — Returns all shots across all projects.
    
-  GET /api/projects/<project_id>/shots — Returns shots for a specific project.
    
-   PATCH/api/projects/<project_id>/shots/<shot_id>— Updates the status of a shot.
    
-   GET /api/projects/<project_id>/assets — Returns assets for a specific project.

-   GET /api/usersProjects — Returns all user–project assignments.
    
-   GET /api/projects/<project_id>/share — Generates or retrieves a share code for a project.
    
-   POST /api/join_project — Allows a user to join a project using a share code.


# 5.2 Error and Exception Handling

Error handling is implemented at multiple layers:

-   Frontend: Displays user-friendly error messages based on HTTP response codes.
    
-   Backend: Validates requests and returns consistent error messages in JSON format with appropriate HTTP status codes (e.g., 400 for bad input, 401 for unauthorized access, 500 for server errors).
    
-   Database layer: Errors in query execution are caught and translated into meaningful messages before being returned.

# 5.3 Security and Authentication Methods

Authentication and access control are managed through the following mechanisms:

-   Password Security: All user passwords are hashed before being stored in the database using a secure hashing algorithm (e.g., bcrypt).
    
-   Login Verification: On login, hashed passwords are compared securely with stored values.

# 5.4 External Interfaces: TIK Manager Integration

Tracktor includes a plugin-based integration with TIK Manager, a DCC pipeline tool used in VFX production.

-   A PyQt-based menu is embedded in the TIK interface.
    
-   The plugin acts as a Python client that communicates with the Flask backend using HTTP requests.
    
-   Through the TIK endpoint, the TIK plugin can pull or push project data such as shots and assets.
    
-   This functionality is modeled after existing TIK integrations with ShotGrid and Kitsu, and is intended to support synchronization of production data between TIK and the tracker.

# 6. User interface design

The user interface design section focuses on how users interact with the software system. This includes details about the user interface's layout, navigation, functionality, and specific design considerations or usability requirements.
The main goal for the MVP UI is to make it clear enough to be usable. While, better UI design and UX are on the roadmap for this projects, they are a non-goals for the thesis.
 
# 6.1 Wireframes or mockups of key screens

Tracktor is designed to be a multipage and multiuser web application, which considerably impacts the design of the User Interface.

The pages are mainly structured into a Login Page, a User's Dashboard, Project Page and Item Page.

![UI sketches](https://livebournemouthac-my.sharepoint.com/:i:/g/personal/s5221034_bournemouth_ac_uk/ERMdcf563s1FhRcaE-C1tw4BSVAZvT__Eo-mmbaMcRvYaQ?e=4vjBUc)

![UI sketches 2](https://livebournemouthac-my.sharepoint.com/:i:/g/personal/s5221034_bournemouth_ac_uk/EcnnGTtXL7NMsNp7Cvitf6gBpkQRJc-8nseC4Loc_zkv3Q?e=sPwe4d)

# 6.2 Description of user workflows and interactions

Tracktor UI is built to work, in a way, like a directory structure. After login in the user has a path to get to it desired location. The UI asks the user to fill in the fields and create project/asset/shot with the click of the button.

# 7. Deployment Plan


# 7.1 Tracktor Deployment

The deployment process for this project leverages Docker to containerize both the frontend (React) and backend (Flask) into a single, portable application image. This approach simplifies the setup, ensures environment consistency, and provides a professional, scalable foundation for future development.

### Containerization with Docker

The application is composed of two main components:

-   A React frontend, responsible for the user interface
    
-   A Flask backend, handling the API logic and data processing

These components are packaged together using a single Dockerfile. The React app is compiled into static files (npm run build) and served directly by the Flask application. This ensures that both the UI and API are served from the same origin, simplifying development and deployment.
  
### Deployment Platform

To host the application for demonstration purposes and while growing it into a bigger app, I aim to use a free-tier cloud platform such as Render, Fly.io, or Railway. These platforms support Docker-based deployments and allow the entire containerized application to be deployed with minimal setup.

### Scalability and Future Hosting

While this deployment strategy is suitable for demonstration and early development stages, the use of Docker enables smooth migration to more advanced hosting environments in the future.
  

# 7.2 TIK Plugin Deployment

Since the Tracktor plugin for TIK is borrowing its structure from already existing Shotgrid and Kitsu integrations, so the prepared plugin files need to be copied into the respective folders. To simplify the process for the user, the plugin folder includes the installation script, which will do it for the user. The user only needs to provide an installation directory where they have their TIK plugin.

# 8. Assumptions and Dependencies

The development of this application is also based on some critical assumptions about who is going to use it, how and in what way. Here is an non-exhaustive list of those dependancies:

- Users will have a modern browser (e.g., Chrome, Firefox) with JavaScript enabled.

- Users will be connected to the internet to access the app and interact with the backend.

- Each user is assumed to work on small to mid-sized teams, with limited concurrency.

- If the TIK integration is used, the user must have TIK installed on their machine.

- The user understands basic project structure (shots, assets, statuses, etc.).

- Each user will access only their own projects, with access control based on login credentials.

- The changes to the project data will be made one at a time, even if multiple users have access to it.

- For plugin features, the user is expected to manually run the installer into their TIK setup.

# 9. Future Work

Since Tracktor is an ongoing opensource development project, as well as being part of the Mater's thesis, a separate MVP has been defined for both states. The so-called Core MVP for the webapp and the TIK plugin are the prospected deliverables for the Master's Thesis, while any further improvement and features are included in the general roadmap for the project.

Roadmap for the Tracktor webapp:

- Review functionality

- Version control information

- File sharing

- Better UI

- Elaborate role division

 
Roadmap for the TIK integration plugin: 

- Push updates into the web app, like version control
