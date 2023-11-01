import uvicorn


if __name__ == "__main__":
    uvicorn.run('axdocsystem.src.app:app', reload=True, port=4141)

