# Donation Management API

## Overview
This API provides endpoints for managing donations, users, receipts, and drop-off sites. It allows users to register, log in, donate items, reserve donations, upload proof of donations, and manage receipts.

## Features
- User authentication (Register, Login, Edit Profile, Reset Password)
- Manage donations (Create, Retrieve, Update, Reserve, Cancel)
- Upload proof of donations and receipts
- Track donation history and reserved donations
- Retrieve non-admin users

## API Endpoints

### Authentication & User Management
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/register/` | POST | Register a new user |
| `/login/` | POST | Login user |
| `/edituser/` | PATCH | Edit user details |
| `/resetpassword/` | POST | Reset user password |
| `/members/` | GET | Retrieve a list of non-admin users |

### Donations
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/donations/` | GET, POST | Retrieve all donations / Create a new donation |
| `/donations/<int:pk>/status/` | PATCH | Update donation status |
| `/donations/mine/` | GET | Retrieve user’s own donations |
| `/donations/<int:donation_id>/` | GET | Retrieve a specific donation’s details |
| `/donations/<int:donation_id>/reserve/` | POST | Reserve a donation |
| `/donations/reserved/` | GET | Retrieve donations reserved by the user |
| `/donations/<int:donation_id>/cancel/` | POST | Cancel a reserved donation |

### Proof & Receipts
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/donations/<int:donation_id>/proof/` | POST | Upload proof for a donation |
| `/receipts/` | GET | Retrieve receipt history |
| `/donations/<int:donation_id>/receipt/` | POST | Upload a receipt for a donation |

### Drop-off Sites
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dropoff-sites/` | GET | Retrieve list of drop-off sites |

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run database migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Configuration
- Ensure that your `.env` file is correctly set up with required environment variables.
- Configure CORS settings to allow frontend access.
- Set up media file handling for proof and receipts storage.

## License
This project is licensed under the MIT License.

## Contribution
Feel free to submit issues or pull requests to improve the project.

## Contact
For questions or collaboration, contact [your email].

