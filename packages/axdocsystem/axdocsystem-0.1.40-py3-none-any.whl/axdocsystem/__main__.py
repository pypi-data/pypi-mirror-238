import uvicorn
from axdocsystem.src.app import app


if __name__ == "__main__":
    uvicorn.run(app, port=4141)

