# Django Blog App with HTMX

![logo](/logo.png)

A modern and dynamic blog application built using **Django** and **HTMX**. This project demonstrates the integration of HTMX for building interactive and seamless user experiences without relying heavily on JavaScript frameworks.

## Features

- **HTMX Integration**: Enhance the user experience with partial page updates and AJAX-like behavior without writing JavaScript.
- **Post Creation and Editing**: Add, edit, and delete blog posts dynamically with inline forms.
- **Comments System**: Add, delete, and update comments without reloading the page.
- **User Authentication**: Register, log in, and log out functionality for users.
- **Responsive Design**: The UI is responsive and mobile-friendly.

## Technologies Used

- **Django**: Backend framework.
- **HTMX**: Frontend interactivity for handling requests and updates.
- **Bootstrap**: For responsive and modern UI design.
- **SQLite**: Default database for development.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Django 4.x
- HTMX

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/django-blog-htmx.git
   cd django-blog-htmx
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: `env\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply the migrations:

   ```bash
   python manage.py migrate
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

6. Open the app in your browser:

   ```
   http://127.0.0.1:8000/
   ```

### Usage

- Create a new post, edit existing posts, and add comments to any post. All updates are handled smoothly using HTMX for a better user experience.

## Project Structure

