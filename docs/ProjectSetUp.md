# Project setup

## 1. Create a new directory for your project and navigate into it

```bash
mkdir flask-strawberry-mongo-demo
cd flask-strawberry-mongo-demo
```

## 2. Create a virtual environment and activate it

It’s best practice to use a virtual environment for each Python project. This isolates your project’s dependencies from other projects or the system Python, avoids version conflicts, and makes it easier to share your project with others.

```bash
python -m venv venv        # Create a virtual environment

# Activate it:
# Windows (command prompt):
.venv\Scripts\ctivate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Git Bash on Windows
source venv/Scripts/activate

# Linux/MacOS:
source venv/bin/activate
```

While activated, any packages you install will only affect this project.

### Why Create a Virtual Environment?

1. **Isolate Dependencies**  
   Each Python project may need different libraries or versions. A virtual environment ensures your project’s dependencies don’t conflict with others.

2. **Avoid System Pollution**  
   Installing packages globally can clutter your system Python and might require admin rights. A venv keeps them local.

3. **Reproducibility**  
   Using `requirements.txt`, others can recreate the same environment with `pip install -r requirements.txt`.

4. **Safe Experimentation**  
   You can try new packages or versions without affecting other projects or your system Python.

## 3. Install Required Dependencies

With the virtual environment active, install Flask, Strawberry GraphQL, Flask-PyMongo, and PyMongo:

```bash
pip install Flask strawberry-graphql flask-pymongo pymongo
```

### Explanation of Each Package

- **Flask** – A lightweight WSGI web framework for building web applications and APIs.
- **strawberry-graphql** – A modern Python library for creating GraphQL APIs with simple and type-safe schemas.
- **flask-pymongo** – A Flask extension that integrates PyMongo, making it easier to connect Flask with MongoDB.
- **pymongo** – The official MongoDB driver for Python, providing low-level database interaction.

## 4. Save Dependencies to requirements.txt

After installing the packages, generate a requirements.txt file so others (or yourself on another machine) can recreate the same environment:

```bash
pip freeze > requirements.txt
```

Example content of `requirements.txt`:

```ini
Flask==2.3.2
strawberry-graphql==0.211.0
flask-pymongo==2.3.0
pymongo==4.7.0
```

Others can install the same packages with:

```bash
pip install -r requirements.txt
```

## 5. Add `.gitignore`

Make sure to ignore your virtual environment folder in Git so it doesn’t get committed to the repository.

Add this to your `.gitignore` file:

```bash
venv/
```

This ensures that only your code and requirements.txt are tracked, while the virtual environment (which can be recreated anytime) is excluded.

---

**Important:**

- Run `pip install` commands only after creating and activating the virtual environment.
- If the virtual environment is not active, packages will be installed globally on your system Python, which may cause conflicts with other projects.

## 6. Deactivate the virtual environment

When you’re done working on your project, you can deactivate the virtual environment to return to the global Python environment:

```bash
deavtivate
```

👉 After deactivating, your terminal will no longer show (venv) in the prompt, meaning you’re back to the system Python.
