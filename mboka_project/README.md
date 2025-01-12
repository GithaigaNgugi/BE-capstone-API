# Task Management API

This is a Django RESTful API designed to manage tasks in service industries. The API supports user roles (Manager, Technician, and Client), with role-based permissions for creating, updating, viewing, and deleting tasks. It also provides user authentication using token-based authentication.

---

## Features

- **User Roles**: Manager, Technician, Client.
- **Role-Based Permissions**:
  - **Manager**: Full CRUD operations on tasks and the ability to assign tasks to technicians.
  - **Technician**: Can create, read, and update tasks but cannot delete them.
  - **Client**: Read-only access to specific fields of tasks.
- **Task CRUD Operations**.
- **Authentication**: Token-based authentication.
- **Validation**: Ensures that tasks cannot be created with a due date earlier than the current date.

---

## Endpoints

### 1. **Authentication Endpoints**

#### **Register User**
- **Path**: `/api/auth/register/`
- **Method**: `POST`
- **Description**: Registers a new user with a specified role.
- **Request Example**:
  ```json
  {
    "username": "manager_user",
    "password": "password123",
    "role": "manager"
  }
  ```
- **Response Example**:
  ```json
  {
    "username": "manager_user",
    "role": "manager",
    "id": 1
  }
  ```

#### **Obtain Auth Token**
- **Path**: `/api/auth/token/`
- **Method**: `POST`
- **Description**: Obtains an authentication token using the user's credentials.
- **Request Example**:
  ```json
  {
    "username": "manager_user",
    "password": "password123"
  }
  ```
- **Response Example**:
  ```json
  {
    "token": "your-auth-token-here"
  }
  ```

---

### 2. **Task Endpoints**

#### **List Tasks**
- **Path**: `/api/tasks/`
- **Method**: `GET`
- **Description**: Retrieves a list of tasks. Accessible by all roles.
- **Response Example (Manager)**:
  ```json
  [
    {
      "id": 1,
      "title": "Fix server issue",
      "description": "Resolve database connection errors",
      "due_date": "2024-01-15",
      "priority": "high",
      "status": "pending",
      "created_by": 1,
      "assigned_to": 2
    }
  ]
  ```
- **Response Example (Client)**:
  ```json
  [
    {
      "id": 1,
      "title": "Fix server issue",
      "description": "Resolve database connection errors",
      "status": "pending"
    }
  ]
  ```

#### **Create Task**
- **Path**: `/api/tasks/`
- **Method**: `POST`
- **Description**: Creates a new task. Only accessible by Managers and Technicians.
- **Request Example**:
  ```json
  {
    "title": "Fix server issue",
    "description": "Resolve database connection errors",
    "due_date": "2024-01-15",
    "priority": "high",
    "status": "pending",
    "assigned_to": 2
  }
  ```
- **Response Example**:
  ```json
  {
    "id": 1,
    "title": "Fix server issue",
    "description": "Resolve database connection errors",
    "due_date": "2024-01-15",
    "priority": "high",
    "status": "pending",
    "created_by": 1,
    "assigned_to": 2
  }
  ```

#### **Retrieve Task**
- **Path**: `/api/tasks/{task_id}/`
- **Method**: `GET`
- **Description**: Retrieves a specific task by its ID. Accessible by all roles.
- **Response Example**:
  ```json
  {
    "id": 1,
    "title": "Fix server issue",
    "description": "Resolve database connection errors",
    "due_date": "2024-01-15",
    "priority": "high",
    "status": "pending",
    "created_by": 1,
    "assigned_to": 2
  }
  ```

#### **Update Task**
- **Path**: `/api/tasks/{task_id}/`
- **Method**: `PUT` or `PATCH`
- **Description**: Updates a specific task. Accessible by Managers and Technicians.
- **Request Example**:
  ```json
  {
    "status": "completed"
  }
  ```
- **Response Example**:
  ```json
  {
    "id": 1,
    "title": "Fix server issue",
    "description": "Resolve database connection errors",
    "due_date": "2024-01-15",
    "priority": "high",
    "status": "completed",
    "created_by": 1,
    "assigned_to": 2
  }
  ```

#### **Delete Task**
- **Path**: `/api/tasks/{task_id}/`
- **Method**: `DELETE`
- **Description**: Deletes a specific task. Only accessible by Managers.
- **Response Example**:
  ```json
  {}
  ```

---

## Role-Based Permissions

1. **Manager**
   - Full CRUD operations on tasks.
   - Can assign tasks to Technicians.
   - Can view all task details.

2. **Technician**
   - Can create, read, and update tasks.
   - Cannot delete tasks.

3. **Client**
   - Read-only access.
   - Can view only `title`, `description`, and `status` of tasks.

---

## Error Handling

- **400 Bad Request**: Returned when required fields are missing or invalid data is provided.
- **401 Unauthorized**: Returned when the authentication token is missing or invalid.
- **403 Forbidden**: Returned when a user tries to perform an action they do not have permission for.
- **404 Not Found**: Returned when a requested task is not found.

---

## Validation

- Ensures that the `due_date` field is always greater than the current date when creating or updating a task.

---

## Testing the API using Postman

1. **Import Endpoints**: Create a Postman collection with all the above endpoints.
2. **Set Authorization**: Use Bearer Token authentication and pass the token in the `Authorization` header.
3. **Test Role Permissions**:
   - Register different users (Manager, Technician, Client) and test the endpoints according to their permissions.

---

## Sample Postman Request Headers

```http
Authorization: Bearer your-auth-token-here
Content-Type: application/json
```

---

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/GithaigaNgugi/BE-capstone-API.git
   ```

2. Navigate to the project directory:
   ```bash
   cd BE-capstone-API
   ```

3. Set up a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Apply migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Use Postman or any API client to interact with the endpoints.

---

## License

This project is licensed under the MIT License.

---

## Author

**Brian Githaiga Ngugi**

For any inquiries or contributions, feel free to reach out!

+254714417763