from pprint import pprint

import click
from flask import current_app
from flask.cli import with_appcontext

from oarepo_runtime.cli import oarepo
from oarepo_runtime.datastreams import StreamEntry
from oarepo_runtime.datastreams.fixtures import (
    FixturesResult,
    dump_fixtures,
    load_fixtures,
)
from oarepo_runtime.uow import BulkUnitOfWork


@oarepo.group()
def fixtures():
    """Load and dump fixtures"""


@fixtures.command()
@click.argument("fixture_dir", required=False)
@click.option("--include", multiple=True)
@click.option("--exclude", multiple=True)
@click.option("--system-fixtures/--no-system-fixtures", default=True, is_flag=True)
@click.option("--show-error-entry/--hide-error-entry", is_flag=True)
@click.option(
    "--bulk/--no-bulk",
    is_flag=True,
    default=True,
    help="Use bulk indexing (that is, delay indexing)",
)
@click.option(
    "--bulk-size",
    default=100,
    help="Size for bulk indexing - this number of records "
    "will be committed in a single transaction and indexed together",
)
@with_appcontext
def load(
    fixture_dir=None,
    include=None,
    exclude=None,
    system_fixtures=None,
    show_error_entry=False,
    bulk=True,
    bulk_size=100,
):
    """Loads fixtures"""
    if show_error_entry:

        def error_callback(entry: StreamEntry):
            pprint(entry.entry)
            for err in entry.errors:
                print(err.code)
                print(err.message)
                print(err.info)

    else:
        error_callback = None

    with current_app.wsgi_app.mounts["/api"].app_context():
        results: FixturesResult = load_fixtures(
            fixture_dir,
            _make_list(include),
            _make_list(exclude),
            system_fixtures=system_fixtures,
            error_callback=error_callback,
            batch_size=bulk_size,
            uow_class=BulkUnitOfWork if bulk else None,
        )
        _show_stats(results, "Load fixtures")


@fixtures.command()
@click.option("--include", multiple=True)
@click.option("--exclude", multiple=True)
@click.argument("fixture_dir", required=True)
@with_appcontext
def dump(fixture_dir, include, exclude):
    """Dump fixtures"""
    with current_app.wsgi_app.mounts["/api"].app_context():
        results = dump_fixtures(fixture_dir, _make_list(include), _make_list(exclude))
        _show_stats(results, "Dump fixtures")


def _make_list(lst):
    return [
        item.strip() for lst_item in lst for item in lst_item.split(",") if item.strip()
    ]


def _show_stats(results: FixturesResult, title: str):
    print(f"{title} stats:")
    print(f"    ok records: {results.ok_count}")
    print(f"    failed records: {results.failed_count}")
    print(f"    skipped records: {results.skipped_count}")
    print()
    print("Details:")
    for fixture, r in results.results.items():
        print(
            f"    {fixture} - {r.ok_count} ok, {r.failed_count} failed, {r.skipped_count} skipped"
        )
