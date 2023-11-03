import click

from kt2.commands import KoppeltaalCli, pass_koppeltaal


@click.group()
@click.option("--debug", is_flag=True, help="enable debug logs ( default: False )")
@click.option("--config", default="koppeltaal.toml", help="select config file")
@click.pass_context
def cli(ctx, **kwargs):
    """Koppeltaal command line tool"""
    ctx.obj = KoppeltaalCli(**kwargs)


@cli.command("patients", short_help="get all patient resources from koppeltaal api")
@pass_koppeltaal
def patients(koppeltaal: KoppeltaalCli, **kwargs):
    koppeltaal.patients(**kwargs)


@cli.command(
    "patient", short_help="get single patient resource by id from koppeltaal api"
)
@click.option("--id", help="id of the patient", required=True)
@pass_koppeltaal
def patient(koppeltaal: KoppeltaalCli, **kwargs):
    koppeltaal.patient(**kwargs)


@cli.command(
    "practitioners", short_help="get all practitioner resources from koppeltaal api"
)
@pass_koppeltaal
def practitioners(koppeltaal: KoppeltaalCli, **kwargs):
    koppeltaal.practitioners(**kwargs)


@cli.command(
    "practitioner",
    short_help="get single practitioner resource by id from koppeltaal api",
)
@click.option("--id", help="id of the practitioner", required=True)
@pass_koppeltaal
def practitioner(koppeltaal: KoppeltaalCli, **kwargs):
    koppeltaal.practitioner(**kwargs)


@cli.command("endpoints", short_help="get all endpoint resources from koppeltaal api")
@pass_koppeltaal
def endpoints(koppeltaal: KoppeltaalCli, **kwargs):
    koppeltaal.endpoints(**kwargs)


@cli.command(
    "endpoint",
    short_help="get single endpoint resource by id from koppeltaal api",
)
@click.option("--id", help="id of the endpoint", required=True)
@pass_koppeltaal
def endpoint(koppeltaal: KoppeltaalCli, **kwargs):
    koppeltaal.endpoint(**kwargs)


@cli.command(
    "activitydefinitions",
    short_help="get all activitydefinition resources from koppeltaal api",
)
@pass_koppeltaal
def activitydefinitions(koppeltaal: KoppeltaalCli, **kwargs):
    koppeltaal.activitydefinitions(**kwargs)


@cli.command(
    "activitydefinition",
    short_help="get single activitydefinition resource by id from koppeltaal api",
)
@click.option("--id", help="id of the activitydefinition", required=True)
@pass_koppeltaal
def activitydefinition(koppeltaal: KoppeltaalCli, **kwargs):
    koppeltaal.activitydefinition(**kwargs)


@cli.command(
    "delete_activitydefinition",
    short_help="get single activitydefinition resource by id from koppeltaal api",
)
@click.option("--id", help="id of the activitydefinition", required=True)
@pass_koppeltaal
def delete_activitydefinition(koppeltaal: KoppeltaalCli, **kwargs):
    koppeltaal.delete_activitydefinition(**kwargs)


@cli.command(
    "tasks",
    short_help="get all task resources from koppeltaal api",
)
@pass_koppeltaal
def tasks(koppeltaal: KoppeltaalCli, **kwargs):
    koppeltaal.tasks(**kwargs)


@cli.command(
    "task",
    short_help="get single task resource by id from koppeltaal api",
)
@click.option("--id", help="id of the task", required=True)
@pass_koppeltaal
def task(koppeltaal: KoppeltaalCli, **kwargs):
    koppeltaal.task(**kwargs)


@cli.command("info", short_help="show Koppeltaal api info")
@pass_koppeltaal
def info(koppeltaal: KoppeltaalCli):
    koppeltaal.info()


@cli.command("version", short_help="show Koppeltaal cli version")
@pass_koppeltaal
def version(koppeltaal: KoppeltaalCli):
    koppeltaal.show_version()


if __name__ == "__main__":
    cli()
