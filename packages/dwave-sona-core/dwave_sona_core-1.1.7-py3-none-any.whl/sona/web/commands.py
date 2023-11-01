import typer
import uvicorn

from .server import api

app = typer.Typer()


@app.command()
def run(host: str = "0.0.0.0", port: int = 8080):
    uvicorn.run(api, host=host, port=port, log_level="info")
