try:
    import sqlalchemy
    print("SQLAlchemy imported:", sqlalchemy.__version__)
    from sqlalchemy.orm import Session
    print("SQLAlchemy Session imported successfully")
except ImportError as e:
    print("Error importing SQLAlchemy:", e)
except Exception as e:
    print("Other error:", e)
