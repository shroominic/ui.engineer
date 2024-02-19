from .core import app as app


if __name__ == "__main__":
    try:
        import uvicorn

        uvicorn.run(app)
    except ImportError:
        pass
