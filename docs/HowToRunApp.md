# How to Run the App

## 1. **Set up a virtual environment** (optional but recommended):

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

## 2. Install Dependencies

If you already have a `requirements.txt`, you don’t need to reinstall dependencies if they are already installed in your environment. To ensure everything is up to date, you can still run:

```bash
pip install -r requirements.txt
```

This will install any missing packages or update outdated ones without reinstalling everything unnecessarily.

If you don't have `requirements.txt` insltall the following

```bash
pip install Flask strawberry-graphql pymongo
```

## 3. **Run the Flask app**:

```bash
python app.py
```

## 4. **Access the app**:

- Home route: `http://127.0.0.1:5050/`
- GraphQL endpoint (interactive): `http://127.0.0.1:5050/graphql`
- From another device on the same network: `http://<your-computer-ip>:5050/`
