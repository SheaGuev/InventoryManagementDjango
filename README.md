Here's a README file for the InventoryManagementDjango repository, based on the coursework details and the repository content:

# CSE Equipment Inventory Management System

This web-based inventory application is designed to track the number and type of assets available and manage the loan of assets for the School of Computer Science and Engineering's Technical Unit. The project is developed using Django framework with SQLite database.
##Deployment
The website can be accessed at https://sheasexton.pythonanywhere.com/login
To experience the application from a user perspective, log in with:
Username: example@mail.com
Password: Test123test
##Note: Most functionalities require admin approval, and admin account can be created upon request; if not then install locally and create a superuser to test the full functionality.
## Features

### User Management
- User registration and account management (design only, not implemented)
- Secure login functionality
- User roles: Regular users and Admin users

### Equipment Management
- View list of equipment
- Filter equipment by availability, return date, and type
- Sort equipment by predefined fields
- Search for equipment based on ID, Asset Tag, name, or type
- Reserve/book equipment (design only, not implemented)
- View current and historical bookings
- Cancel reservations
- Easily re-book from historical bookings
- Designation of on-site use only items

### Admin Functionalities
- Separate admin area with enhanced access
- Add new equipment with details
- Update existing equipment details
- Manage user accounts (approve signups, add/remove/update roles)
- Generate reports (inventory status, usage history, warranty, overdue equipment)
- Get inventory counts by various categories

### Non-functional Requirements
- Separation of business and application logic
- Django-based implementation
- SQLite database storage
- User-friendly and intuitive interface
- Data encryption (design only, not implemented)
- Backup and recovery capabilities (design only, not implemented)

## Project Structure
The project follows Django's recommended structure:

- `InventoryManagement/`: Main project directory
- `authentication/`: App for user authentication
- `InventoryManagementWestminster/`: Main app for inventory management
- `static/`: Static files (CSS, JavaScript, images)
- `manage.py`: Django's command-line utility for administrative tasks

## Setup and Installation
1. Clone the repository
2. Install required dependencies “pip install django django-bootstrap-v5
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the development server: `python manage.py runserver`

## Usage
- Access the admin panel at `/admin/`
- Regular users can access the main application interface
- Admins have additional functionalities accessible through the admin panel

## Contributing
This project is part of a university coursework. Contributions should adhere to the guidelines provided in the coursework brief.

## License
This project is for educational purposes only and is not licensed for commercial use.

## Acknowledgements
Developed as part of the Software Development Group Project (5COSC021W) at the University of Westminster, School of Computer Science and Engineering.

---

Note: This README is based on the coursework brief and the repository structure. Some features mentioned may be in design phase only and not fully implemented in the current codebase
