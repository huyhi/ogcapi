import click
from click import core

from client.constant import JSON_TYPE
from client.ogcclient import OgcApiClient

MAX_CLI_OUT_LEN = 200
MAX_CLI_OUT_LINES = 5


@click.group()
@click.option('--host', help='set request server host')
@click.option('--accept-type', default=JSON_TYPE, help='set accepted response content type')
@click.option('--show-all', is_flag=True, default=False, help='show all response from server')
@click.option('--collection-id', help='collection id')
@click.pass_context
def entrance(
        ctx: core.Context,
        host: str,
        accept_type: str,
        show_all: bool,
        collection_id: str
):
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj['host'] = host
    ctx.obj['accept_type'] = accept_type
    ctx.obj['show_all'] = show_all
    ctx.obj['collection_id'] = collection_id


@entrance.command('desc')
@click.pass_context
def desc(ctx):
    click.echo(
        click_out(ctx, get_client(ctx).desc())
    )


@entrance.command('conformance')
@click.pass_context
def conformance(ctx):
    click.echo(
        click_out(ctx, get_client(ctx).conformance())
    )


@entrance.command('list_collections')
@click.pass_context
def list_collections(ctx):
    click.echo(
        click_out(ctx, get_client(ctx).list_collections())
    )


@entrance.command('get_collection_by_id')
@click.pass_context
def get_collection_by_id(ctx):
    collection_id = ctx.obj['collection_id']
    click.echo(
        click_out(ctx, get_client(ctx).get_collection_by_id(collection_id))
    )


@entrance.command('list_collection_items_by_id')
@click.pass_context
def list_collection_items_by_id(ctx):
    collection_id = ctx.obj['collection_id']
    click.echo(
        click_out(ctx, get_client(ctx).list_collection_items_by_id(collection_id))
    )


def get_client(ctx: core.Context) -> OgcApiClient:
    return OgcApiClient(**{
        'host': ctx.obj['host'],
        'accept_type': ctx.obj['accept_type']
    })


def click_out(ctx: core.Context, raw_resp: str) -> str:
    if ctx.obj['show_all']:
        return raw_resp

    ret = raw_resp
    is_show_less = False
    # max show 200 characters or 5 lines
    raw_resp_len = len(raw_resp)
    if raw_resp_len > MAX_CLI_OUT_LEN:
        ret = ret[:MAX_CLI_OUT_LEN]
        is_show_less = True

    ret_in_lines = ret.split('\n')
    if len(ret_in_lines) > MAX_CLI_OUT_LINES:
        ret = '\n'.join(ret_in_lines[:MAX_CLI_OUT_LINES])
        is_show_less = True

    if is_show_less:
        ret = '{} \n ... [{} characters in all]'.format(ret, raw_resp_len)
    return ret
