# GenAss

## Overview

GenAss is a project consisting of two Django REST Framework (DRF) applications that securely communicate by sending and receiving encrypted messages. The project focuses on building secure APIs using middleware for encryption/decryption, along with features like user authentication and a management dashboard.

Key functionalities include:

- **User Authentication**: Registration and login capabilities for each application.
- **Secure Messaging**: Encrypted message transmission between the two applications.
- **Middleware Security**: middleware for encryption, decryption, and request validation.
- **Dashboard**: An intuitive interface to manage users and messages.

---

## Key Features

1. **Login and Registration**:
   - Secure user authentication using Django's built-in authentication system.

2. **Sending and Receiving Messages**:
   - Encrypted API-based message transmission between applications.

3. **Security Enhancements**:
   - Middleware for encryption/decryption and request validation.

4. **User and Message Management**:
   - Dashboards to manage user accounts and view messages.

---

## Technology Stack

- **Backend**: Django REST Framework
- **Frontend**: Vue.js
- **Encryption**: Fernet symmetric encryption from the `cryptography` library
- **Middleware**: Custom Django middleware for security enhancements
- **Database**: SQLite 


---

## Middleware Implementation

Below is an example middleware implementation for secure message communication:

```python
from cryptography.fernet import Fernet
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import json

class MessageEncryptionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        # Initialize the cipher with the encryption key from settings
        self.key = settings.ENCRYPTION_KEY
        self.cipher = Fernet(self.key)
        super().__init__(get_response)

    def process_request(self, request):
        # Check if the request content type is JSON
        if request.content_type == 'application/json' and request.body:
            try:
                # Decode the incoming request body into JSON
                request_data = json.loads(request.body.decode('utf-8'))
                
                if 'message' in request_data:
                    encrypted_content = request_data['message']
                    print(f"Encrypted message in request: {encrypted_content}")  # Debugging
                    
                    # Decrypt the message content
                    decrypted_content = self.cipher.decrypt(encrypted_content.encode()).decode('utf-8')
                    print(f"Decrypted message: {decrypted_content}")  # Debugging
                    
                    # Replace the encrypted message with the decrypted content
                    request.data = request_data
                    request.data['message'] = decrypted_content
            except Exception as e:
                print(f"Error processing request: {e}")  # Error handling for decryption failure

    def process_response(self, request, response):
        # Check if the response has the 'message' field and is JSON
        if hasattr(response, 'data') and isinstance(response.data, dict) and 'message' in response.data:
            message_content = response.data['message']
            print(f"Original message before decryption: {message_content}")  # Debugging
            
            # Encrypt the message content before returning it (for response encryption)
            try:
                encrypted_content = self.cipher.encrypt(message_content.encode('utf-8')).decode('utf-8')
                print(f"Encrypted message in response: {encrypted_content}")  # Debugging
                
                # Set the encrypted message back in the response
                response.data['message'] = encrypted_content
            except Exception as e:
                print(f"Error encrypting message in response: {e}")
                response.data['message'] = "Error encrypting message"
        
        return response


## Setup Instructions

### Prerequisites
**Python: Version 3.8 or higher**
**Node.js and npm: For frontend development**


### Backend Setup
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   ```
2. **Navigate to the backend Directory:**:
   ```bash
   cd IT120-final-Project/backend
   ```

3. **Setup Virtual Environment**:
   ```bash
   python -m venv venv

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables:**:
   - Create a .env file in the backend directory with the following variable:
   ENCRYPTION_KEY=your_generated_encryption_key


6. **Generate a Fernet Key**:
   ```python
   from cryptography.fernet import Fernet
   print(Fernet.generate_key().decode())
   ```
7. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Run the Development Server:**:
     ```bash
     python manage.py runserver
     ```

### Frontend Setup
1. **Navigate to the Frontend Directory:**:
   ```bash
   cd IT120-final-Project/frontend
   ```

2. **Install Dependencies:**:
   ```bash
   npm install
   ```

3. **Run the Development Server:**:
   ```bash
   npm run dev
   ```

### FrontendV2 Setup
1. **Navigate to the FrontendV2 Directory:**:
   ```bash
   cd IT120-final-Project/frontendV2
   ```

2. **Install Dependencies:**:
   ```bash
   npm install
   ```

3. **Run the Development Server:**:
   ```bash
   npm run dev
   ```

### Usage
1. Access the Application:
   - Backend: `http://127.0.0.1:8000/`
   - Frontend (Student): http://localhost:3000/
   - FrontendV2 (Facilitator): http://localhost:3050/
2. Register a New User:
   - Use the registration interface to create a new user account.
3. Login:
   - Access your account using the login interface.
4. Send Messages:
   - Students can send encrypted messages via the messaging feature.
5. View Messages:
   - Facilitators can view and decrypt messages sent by students.

## Security Considerations
- Keep the encryption key (ENCRYPTION_KEY) secure and out of version control.
- Use HTTPS for production deployment to secure data in transit
- Regularly update dependencies and monitor authentication mechanisms for vulnerabilities.

## Collaboration
This project was collaboratively developed by our group. All contributions and roles are documented in the commit history and project management boards within this repository.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
---
