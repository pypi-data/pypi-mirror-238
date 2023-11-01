import typer
from sona.core.inferencer import InferencerBase
from sona.core.messages.context import Context
from sona.settings import settings

INFERENCER_CLASS = settings.SONA_INFERENCER_CLASS

app = typer.Typer()


@app.command()
def test(inferencer_cls: str):
    inferencer: InferencerBase = InferencerBase.load_class(inferencer_cls)()
    inferencer.on_load()
    ctx = (
        Context(jobs=[inferencer.job_example()])
        if inferencer.job_example()
        else inferencer.context_example()
    )
    next_ctx = inferencer.process(ctx)
    print(next_ctx.results)
