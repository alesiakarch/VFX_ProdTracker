# 1. Introduction and Overview

Tracktor is a web-based VFX production tracking application designed for freelancers, students, and small-sized creative teams. This project was conceived to bridge the gap between professional production tracking tools and the lightweight needs of individuals or small teams. It takes inspiration from established pipeline practices while remaining accessible, open-source, and easy to deploy on personal or shared machines.

While larger studios often rely on commercial solutions like ShotGrid or Kitsu, Tracktor aims to offer a simplified, accessible, and opensource alternative that can be deployed locally or online. Its modular design allows future integration with external tools such as TIK Manager, enabling deeper DCC (Digital Content Creation) integration for asset publishing and version control.

The purpose of this document is to outline the technical and structural design of this project and provide a plan for its development.
The project is also being developed in the scope of the Master's thesis, and hence required a specifically defined MVP for the aforementioned therhis submission, which might or might not include the set out general goals for the project. 

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

    - Enable real-time status tracking across departmental tasks

    - Allow notes to be attached to shots and assets for team collaboration

    This is where the web-app thesis MVP is defined. Further features will be moved into a roadmap, which does not necessary match the Master thesis submission schedule.

    ## Primary features
    To meet the above goals, Tracktor includes the following features:

    - User registration and login system

    - Project dashboard with the ability to create, delete, and view projects

    - UI to add/edit shots and assets within a project

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
    Summary:
    1. Core Requirements
    - These are the essential features the app must support to be usable for production tracking:

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

MAKE A DIAGRAM A high-level diagram of the architecture

# 2.2 Component descriptions

The system consists of several core components, each responsible for a distinct layer of functionality:
    
    - Frontend (React with Tailwind CSS & Headless UI)
      The frontend is a single-page application (SPA) developed using React. It provides the user interface and handles all user interactions. Tailwind CSS and Headless UI are used to implement a responsive and accessible design system. React components are organized into reusable modules (e.g., buttons, forms, layouts).

    - Backend (Flask)
      The backend is built with the Flask web framework in Python. It handles the storing logic, routes API requests, and communicates with the database. Each major data entity (e.g., user, project, shot, asset) is represented as a separate Python module or class for modularity.

    - API (RESTful Endpoints)
      The frontend and backend communicate via RESTful HTTP endpoints defined in backend/main.py. These routes allow clients to perform standard operations such as GET (read), POST (create), PUT (update), and DELETE on application data.
   
    - Database (SQLite, with potential migration to PostgreSQL)
      The application uses a relational database to persist user and project data. The schema currently includes tables for Users, Projects, Shots, and Assets. SQLite is used during development for simplicity, with future potential to migrate to PostgreSQL for scalability.

    - Testing (Flask Backend Unit Tests)
      The backend includes unit and integration tests to validate API behavior and ensure reliability. These tests cover data validation, route logic, and error handling.

TIK plugin also consists of the following:

    - Python based client wrapper for making calles to the API
    - PyQt based shelf UI

# 2.3 Design patterns and architectural styles

The Tracktor system follows a client-server architecture, where the frontend React application acts as the client, and the Flask backend serves as the server exposing RESTful APIs. This clear separation enables independent development, testing, and deployment of the frontend and backend components.

    - RESTful API Design:
    The backend exposes RESTful endpoints to allow standardized communication between the client (React UI), the TIK plugin (Python client), and the backend services. This promotes decoupling and scalability.

    - Layered Architecture:
    The system is divided into distinct layers — presentation (React UI), application logic (Flask routes and business logic classes), and data persistence (SQLite/PostgreSQL). This separation improves maintainability and testability.

    - Design Patterns:

        Model-View-Controller (MVC) Inspired: Although Flask does not enforce MVC strictly, the backend organizes code into models (database classes), views (Flask route handlers), and controllers (business logic inside class methods).

        Repository Pattern: Database access is encapsulated within model classes to isolate data logic from the rest of the application.

        Client Wrapper Pattern: The TIK plugin acts as a client wrapper that encapsulates all communication with the backend API, simplifying plugin UI code and allowing easy changes in API endpoints or authentication methods without affecting UI components.
    
   
# 2.4 Discussion of important design decisions and trade-offs

SQLite vs PostgreSQL:
SQLite was selected for initial development due to its simplicity, zero-configuration setup, and ease of use. However, it has limitations in concurrency and scalability. PostgreSQL is planned for future deployment to handle larger datasets, concurrent users, and production robustness. This staged approach reduces complexity during early development but requires future migration planning.

Flask Framework Choice:
Flask was chosen because of its lightweight and flexible nature, which aligns well with the scope of the Tracktor project and developer familiarity. The trade-off is that Flask requires more manual setup and lacks built-in features compared to full-stack frameworks like Django, but this also provides more control and customization.

React with Tailwind and Headless UI:
React enables building a modern and responsive user interface with reusable components. Tailwind CSS provides a utility-first styling approach for fast UI development, while Headless UI components offer accessible interactive elements. This combination accelerates UI development but introduces a learning curve and larger frontend dependencies.

Plugin Communication via REST API:
The TIK plugin is implemented as a Python client that interacts with the backend through RESTful requests. This approach allows plugin UI code to remain lightweight and rely on the existing backend logic, reducing code duplication. The trade-off includes potential latency and network dependency, but the modularity and maintainability benefits outweigh these drawbacks.

# 3. Data Design

The data design defines how Tracktor stores, organizes, and retrieves data across its main entities such as users, projects, shots, and assets. The system uses an SQLite database during development, with potential migration to PostgreSQL for production scalability.

# 3.1 Database Structure and Table Layouts

MAKE A DATABASE DIAGRAM

# 3.2 Data Flow and Storage

Frontend to Backend Flow:
Users interact with the React frontend, which sends POST, GET, PATCH, and DELETE requests to the Flask API. The backend handles these requests, validates input, and performs database operations.

Backend to Database Flow:
The Flask backend interacts with SQLite using sqlite3 queries (or ORM if later switched). It maps the API requests to SQL commands and handles formatting data for API responses.

TIK Plugin Communication:
The Python plugin sends HTTP requests to the Flask backend, just like the frontend. For example, a “Create Project” button in the plugin sends a POST request with project data, which the backend stores in the Projects table.
The data design section focuses on how the software system stores, manages, and processes information, including details about the database structure, data models, and data processing techniques.

# 3.3 Data Validation and Integrity

Validation Rules:

- Usernames must be unique and non-empty.

- Passwords must be hashed before storage.

- Projects must have unique names per user.

- Shot and asset names are validated against duplicates within a project.

Referential Integrity:

- Foreign keys (e.g., owner_id, project_id) are enforced to maintain relationships.

- Cascading deletes may be added to remove associated shots/assets when a project is deleted.

# 3.4 Retrieval Patterns

Projects for a specific user are retrieved by joining Projects and UserProjects using the user_id.

Shots and assets are retrieved based on their project_id, with optional filtering by department status.

All data passed to the frontend or plugin is formatted as JSON via Flask responses.

# 4. Component Design

The component design section provides detailed information about individual modules or components within the system. This includes their specific functionality, what inputs they need and outputs they produce, and any algorithms or data structures they use.

For each major component, consider including:


    - Frontend: React (Tailwind + Headless UI) - Provides the actual web page for the user to interact with. Serves as the UI and the main client. Is written in Javascript + Tailwind CSS

    - Backend: Flask - a class file for each table in database 

    API: RESTful endpoints - main.py for universal REST calls 

    TIK Plugin: Python client using requests to communicate with backend - ui files to display and then functions wraper to call the API

    Database (SQLite, potential for PostgreSQL): Tables for Users, Projects, Shots, Assets - SQLite

    Tests: Tests for Flask backend

Purpose and responsibilities
Input and output specifications
Algorithms and processing logic
Dependencies on other components or external systems

Break down the major parts of your system and describe how each one works.

    User Management:

    /signup: Register new user, store hashed password

    /login: Authenticate user, return session/token

    DB: users(id, username, password_hash)

    Project System:

    DB: projects(id, name, owner_id, deadline, etc.)

    Many-to-many with users via user_project table

    API endpoints: /create_project, /get_projects

    Shot Tracker:

    DB: shots(id, project_id, name, department_statuses...)

    UI: Table with progress per department

    TIK Integration:

    Python plugin UI using PySide2

    Connect to backend via REST API

    Pull/push project data

5. Interface Design (how my app comminicates)

The interface design section describes how different parts of the system will communicate with each other and interact with external systems or services. This includes both internal interfaces between modules and external APIs or integration points.

Key elements to include in the interface design section are:

    API specifications and protocols
    Message formats and data structures
    How errors and exceptions will be handled
    Security and authentication methods

List the main endpoints and what they do:
    5.1 Security and Authentication
    How do users log in? How is access controlled? Are passwords hashed?
        Method	Endpoint	Description
        POST	/login	Authenticates user
        GET	/projects	Returns projects visible to the user
        POST	/projects/create	Create a new project
        POST	/sync/tik	Sync a project from/to TIK

6. User interface design

The user interface design section focuses on how users interact with the software system. This includes details about the user interface's layout, navigation, functionality, and specific design considerations or usability requirements.

Key elements to include in this section are:

Wireframes or mockups of key screens
Description of user workflows and interactions
Accessibility considerations

7. Deployment Plan
(Short term is fine) — Describe:

Local dev setup

Hosting options (Render, Heroku, Docker for Flask)

Manual plugin install for TIK

8. Assumptions and Dependancies
List potential challenges or tech debt you’re aware of. Any prerequisites and requierments of the user and the system.

This tool assumes the project is a shot-based project and that the team size is kept small.

10. Future Work
Mention things that will be tackled in future phases.