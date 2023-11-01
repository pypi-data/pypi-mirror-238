import typer

import cli_sensor
import cli_config
import cli_helper
import cli_measure
import cli_proxy
from import_MRP import __fix_import__
__fix_import__()

#load_dotenv()
app = typer.Typer(add_completion=True)
app.add_typer(cli_sensor.app, name="sensor")
app.add_typer(cli_config.app, name="config")
app.add_typer(cli_measure.app, name="measure")
app.add_typer(cli_proxy.app, name="proxy")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    pass



def run_cli():
    cli_helper.__fix_import__fix_import()
    app()

if __name__ == "__main__":
    run_cli()