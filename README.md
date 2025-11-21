# Artist Portfolio Website

A professional Django-powered portfolio website showcasing an artist's work, featuring artwork galleries, news & events, and newsletter subscription functionality.

## About This Project

This is a full-featured portfolio website built for an artist to showcase their work online. The project demonstrates proficiency in Django web development, including custom admin interfaces, media management, third-party API integration (Mailchimp), and responsive design.

## ✨ Features

### Portfolio Management
- **Artwork Gallery**: Display artworks with detailed information (title, medium, dimensions, year, pricing)
- **Artwork Series**: Organize artworks into themed collections
- **Availability Status**: Track whether pieces are available, sold, or not for sale
- **Image Management**: Upload and manage artwork images with automatic slug generation

### Content Management
- **Artist Profile**: Comprehensive artist biography and contact information
- **Awards & Recognition**: Showcase achievements and accolades
- **Teaching Experience**: Display teaching positions and institutions
- **News & Updates**: Blog-style news posts with rich text editing
- **Events**: Manage and display upcoming and past events

### Marketing & Engagement
- **Newsletter Subscription**: Collect email subscribers with form validation
- **Mailchimp Integration**: Automatic synchronization with Mailchimp audience
- **Contact Form**: Allow visitors to reach out directly
- **Social Media Links**: Integration with Instagram and Facebook

### Admin Features
- **Django Admin Dashboard**: Customized admin interface for content management
- **Django Summernote**: Rich text editor for creating formatted content
- **Media Management**: Organized file upload system for images and documents

## 🛠️ Technology Stack

- **Framework**: Django 5.2.8
- **Database**: PostgreSQL (with psycopg adapter)
- **Image Processing**: Pillow
- **Rich Text Editor**: Django Summernote
- **Email Marketing**: Mailchimp Marketing API
- **Environment Management**: python-dotenv
- **Python Version**: 3.x

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Mailchimp account (for newsletter features)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/rmnpyt/artist-portfolio.git
cd artist-portfolio
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the root directory with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Mailchimp Configuration
MAILCHIMP_API_KEY=your-mailchimp-api-key
MAILCHIMP_SERVER_PREFIX=your-server-prefix
MAILCHIMP_AUDIENCE_ID=your-audience-id
```

### 5. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Collect Static Files
```bash
python manage.py collectstatic
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to view the site and `http://127.0.0.1:8000/admin/` for the admin dashboard.

## 📁 Project Structure

```
├── config/              # Project configuration and settings
├── portfolio/           # Artwork and gallery management
├── content/            # Artist profile, news, and events
├── marketing/          # Newsletter and contact forms
├── templates/          # Base templates
├── static/             # CSS, JavaScript, and images
├── media/              # User-uploaded content
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## 🎯 Key Applications

### Portfolio App
Manages the artist's artwork collection with support for:
- Individual artwork entries
- Series/collection organization
- Availability tracking and pricing
- Image uploads

### Content App
Handles artist information and updates:
- Artist profile and biography
- Awards and achievements
- Teaching experience
- News articles and blog posts
- Event listings

### Marketing App
Facilitates visitor engagement:
- Newsletter subscription system
- Mailchimp API integration
- Contact form functionality
- Email collection and management

## 🔒 Security Notes

**Important**: Before deploying to production:

1. Change the `SECRET_KEY` in settings.py
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS` appropriately
4. Use environment variables for all sensitive data
5. Set up proper database credentials
6. Configure HTTPS/SSL
7. Review Django's deployment checklist: `python manage.py check --deploy`

## 📝 Usage

### Adding Artwork
1. Log in to the admin dashboard
2. Navigate to Portfolio → Artworks
3. Click "Add Artwork"
4. Fill in the details and upload images
5. Save and publish

### Managing Newsletter Subscribers
Subscribers are automatically synced with Mailchimp when they sign up through the website. View and manage subscribers in the admin panel under Marketing → Newsletter Subscribers.

### Creating Content
Use Django Summernote's rich text editor to create formatted news posts and event descriptions with images, links, and styled text.

## 🤝 Contributing
This is a personal portfolio project, but suggestions and feedback are welcome! Feel free to open an issue or submit a pull request.


## 🔗 Connect
- Portfolio Website: [https://azamkashefikia.com]
- GitHub: [https://github.com/rmnpyt]
- LinkedIn: [https://www.linkedin.com/in/raminshirani/]

---
**Note**: This project is continuously being improved. Check back for updates and new features!
