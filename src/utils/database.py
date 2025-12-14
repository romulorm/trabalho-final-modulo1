from sqlmodel import SQLModel, create_engine


sqlite_file_name = "database/db.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

def create_db():
    SQLModel.metadata.create_all(engine)
