# SA-Phase-4-Week-1-Code-Challenge-Superheroes---Compulsory
# Flask Superheroes API

## Description

A Flask-based RESTful API for managing superheroes and their superpowers. This application allows you to track heroes, their powers, and the strength of those powers through a many-to-many relationship. The API supports full CRUD operations and includes email notification capabilities.
---

## Features

- ✅ **Hero Management**: View all heroes or individual hero details with their powers
- ✅ **Power Management**: List all powers, view individual powers, and update power descriptions
- ✅ **Hero-Power Associations**: Create relationships between heroes and powers with strength levels
- ✅ **Data Validation**: Ensures data integrity with validation rules
- ✅ **Email Notifications**: Send emails using Flask-Mail
- ✅ **RESTful Architecture**: Follows REST conventions for clean API design
- ✅ **Proper Error Handling**: Returns appropriate HTTP status codes and error messages

---

## Technologies Used

- **Flask** - Web framework
- **SQLAlchemy** - ORM for database management
- **Flask-Migrate** - Database migrations
- **Flask-Mail** - Email sending functionality
- **SQLite** - Database (can be configured for PostgreSQL or MySQL)
- **SQLAlchemy-Serializer** - Easy model serialization

---

## Database Schema

### Tables

**Heroes**
- `id` (Primary Key)
- `name` (String)
- `super_name` (String)

**Powers**
- `id` (Primary Key)
- `name` (String)
- `description` (String, min 20 characters)

**HeroPowers** (Join Table)
- `id` (Primary Key)
- `hero_id` (Foreign Key → heroes.id)
- `power_id` (Foreign Key → powers.id)
- `strength` (String: 'Strong', 'Weak', or 'Average')

### Relationships
- A Hero has many Powers through HeroPower
- A Power has many Heroes through HeroPower
- HeroPower belongs to both Hero and Power
- Cascade delete configured on HeroPower

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Git

### Installation

1. **Clone the repository**
```bash
   git clone <your-repository-url>
   cd flask-superheroes-api
```

2. **Create and activate a virtual environment**
```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables** (optional, for email functionality)
   
   Create a `.env` file in the root directory:
```bash
   cp .env.example .env
```
   
   Then edit `.env` with your email credentials:
```
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
```

5. **Initialize the database**
```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
```

6. **Seed the database**
```bash
   python seed.py
```
   
   You should see:
```
   Clearing database...
   Creating heroes...
   Creating powers...
   Creating hero powers...
   ✅ Database seeded successfully!
```

7. **Run the application**
```bash
   python app.py
```

   The server will start at `http://127.0.0.1:5555`

---

## API Endpoints

### Heroes

#### `GET /heroes`
Get all heroes (basic info only)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Kamala Khan",
    "super_name": "Ms. Marvel"
  },
  {
    "id": 2,
    "name": "Doreen Green",
    "super_name": "Squirrel Girl"
  }
]
```

#### `GET /heroes/:id`
Get a specific hero with their powers

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Kamala Khan",
  "super_name": "Ms. Marvel",
  "hero_powers": [
    {
      "hero_id": 1,
      "id": 1,
      "power": {
        "description": "gives the wielder the ability to fly through the skies at supersonic speed",
        "id": 2,
        "name": "flight"
      },
      "power_id": 2,
      "strength": "Strong"
    }
  ]
}
```

**Response (404 Not Found):**
```json
{
  "error": "Hero not found"
}
```

---

### Powers

#### `GET /powers`
Get all powers

**Response (200 OK):**
```json
[
  {
    "description": "gives the wielder super-human strengths",
    "id": 1,
    "name": "super strength"
  },
  {
    "description": "gives the wielder the ability to fly through the skies at supersonic speed",
    "id": 2,
    "name": "flight"
  }
]
```

#### `GET /powers/:id`
Get a specific power

**Response (200 OK):**
```json
{
  "description": "gives the wielder super-human strengths",
  "id": 1,
  "name": "super strength"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Power not found"
}
```

#### `PATCH /powers/:id`
Update a power's description

**Request Body:**
```json
{
  "description": "Updated description that is at least 20 characters long"
}
```

**Response (200 OK):**
```json
{
  "description": "Updated description that is at least 20 characters long",
  "id": 1,
  "name": "super strength"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Power not found"
}
```

**Response (400 Bad Request):**
```json
{
  "errors": ["Description must be present and at least 20 characters long"]
}
```

---

### Hero Powers

#### `POST /hero_powers`
Create a new hero-power association

**Request Body:**
```json
{
  "strength": "Average",
  "power_id": 1,
  "hero_id": 3
}
```

**Response (201 Created):**
```json
{
  "id": 11,
  "hero_id": 3,
  "power_id": 1,
  "strength": "Average",
  "hero": {
    "id": 3,
    "name": "Gwen Stacy",
    "super_name": "Spider-Gwen"
  },
  "power": {
    "description": "gives the wielder super-human strengths",
    "id": 1,
    "name": "super strength"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "errors": ["Strength must be one of: Strong, Weak, Average"]
}
```

---

### Email (Bonus Feature)

#### `POST /send-email`
Send an email notification

**Request Body:**
```json
{
  "recipient": "user@example.com",
  "subject": "Hero Update",
  "body": "Your favorite hero has a new power!"
}
```

**Response (200 OK):**
```json
{
  "message": "Email sent successfully"
}
```

**Response (500 Internal Server Error):**
```json
{
  "error": "Error message details"
}
```

---

## Data Validations

### Power Model
- **description**: Must be present and at least 20 characters long
  - Returns: `"Description must be present and at least 20 characters long"`

### HeroPower Model
- **strength**: Must be one of: 'Strong', 'Weak', or 'Average'
  - Returns: `"Strength must be one of: Strong, Weak, Average"`

### Cascade Deletes
- Deleting a Hero will automatically delete all associated HeroPowers
- Deleting a Power will automatically delete all associated HeroPowers

---

## Testing

### Using Postman

1. Import the provided Postman collection:
   - Open Postman
   - Click "Import"
   - Select the `challenge-2-superheroes.postman_collection.json` file

2. Ensure the server is running on port 5555:
```bash
   python app.py
```

3. Run each request in the collection to verify functionality

### Manual Testing Examples

**Test GET /heroes:**
```bash
curl http://127.0.0.1:5555/heroes
```

**Test POST /hero_powers:**
```bash
curl -X POST http://127.0.0.1:5555/hero_powers \
  -H "Content-Type: application/json" \
  -d '{
    "strength": "Strong",
    "power_id": 1,
    "hero_id": 1
  }'
```

**Test PATCH /powers/1:**
```bash
curl -X PATCH http://127.0.0.1:5555/powers/1 \
  -H "Content-Type: application/json" \
  -d '{
    "description": "This is an updated description with more than 20 characters"
  }'
```

---

## Project Structure
```
flask-superheroes-api/
├── app.py                  # Main application file with routes
├── models.py               # Database models and relationships
├── seed.py                 # Database seeding script
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore file
├── migrations/            # Database migration files (created by flask db init)
│   ├── versions/          # Migration version files
│   └── alembic.ini        # Alembic configuration
└── instance/              # Instance folder (created automatically)
    └── app.db            # SQLite database file
```

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Activate your virtual environment and install dependencies
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Email not sending
**Solution:** 
1. Use Gmail App Password (not regular password)
2. Enable 2FA on your Google account
3. Generate App Password in Google Account Settings
4. Update `.env` file with the app password

### Issue: "Table not found" errors
**Solution:** Run migrations and seed
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python seed.py
```

### Issue: Port 5555 already in use
**Solution:** Kill the process or use a different port
```bash
# Kill process on port 5555
lsof -ti:5555 | xargs kill -9

# Or change port in app.py
app.run(port=5556, debug=True)
```

---

## Development Tips

- Use `python app.py` to run in debug mode (auto-reload on changes)
- Check `instance/app.db` to view database contents using DB Browser for SQLite
- Use Postman collections to save time testing
- Review Flask logs in terminal for debugging
- Test edge cases: invalid IDs, missing fields, invalid data

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Acknowledgments

- **Moringa School** for the project requirements and structure
- **Flask Documentation** for excellent guidance
- **SQLAlchemy Community** for robust ORM tools
- All contributors and testers who helped improve this project

---

## Author
- GitHub:https://github.com/donnyMP8
- Email: bigrimanaadonis@gmail.com
- LinkedIn:https://www.linkedin.com/in/adonis-bigirimana-6b7799295/overlay/about-this-profile/

---

**Built using Flask**
