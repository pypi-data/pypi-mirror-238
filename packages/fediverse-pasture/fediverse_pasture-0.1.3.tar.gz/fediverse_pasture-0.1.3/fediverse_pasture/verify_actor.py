import logging
import json
import click
import os

from quart import Quart, request, render_template, redirect

from .data_provider import DataProvider
from .types import Message
from .server import BlueprintForActors
from .server.verify_actor import ActorVerifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_app():
    """Generates the app to be used with an application server

    Usage:

    ```bash
    VERIFY_ACTOR_DOMAIN=my_domain uvicorn --factory fediverse_pasture.verify_actor:get_app
    ```
    """

    return build_app(
        False, os.environ.get("VERIFY_ACTOR_DOMAIN", "localhost:8000"), True
    )


def build_app(only_generate_config: bool, domain: str, https: bool) -> Quart:
    dp = DataProvider.generate_and_load(only_generate_config)
    app = Quart(__name__)

    actor_list = dp.possible_actors + [dp.one_actor]
    app.register_blueprint(BlueprintForActors(actor_list).blueprint)

    async def result_for_actor_uri(actor_uri):
        if not actor_uri:
            return redirect("/")

        message = Message()
        message.add(f"Got Actor Uri {actor_uri}")

        verifier = ActorVerifier(
            actor_list=actor_list, remote_uri=actor_uri, message=message, domain=domain
        )

        if https:
            verifier.scheme = "https"

        result = await verifier.verify()

        if "json" in request.headers.get("accept"):
            return {
                "result": result,
                "messages": json.dumps(message.response, indent=2),
            }

        warnings = []

        if result["alice"]["post_inbox"]:
            result["alice"]["warning"] = True
            warnings.append(
                "Alice should not be able to post to the inbox without \
signing her request."
            )

        if not result["bob"]["get_actor"]:
            result["bob"]["warning"] = True
            warnings.append("Bob should be able to retrieve the actor")
        if not result["claire"]["get_actor"]:
            result["claire"]["warning"] = True
            warnings.append("Claire should be able to retrieve the actor")

        if not result["bob"]["post_inbox"]:
            result["bob"]["warning"] = True
            warnings.append("Bob should be able to post to the inbox")
        if not result["claire"]["post_inbox"]:
            result["claire"]["warning"] = True
            warnings.append(
                """Claire should be able to post to the inbox.
If bob can successfully post to the inbox, this is likely due to using
an unsigned request to retrieve the public key."""
            )

        if not result["webfinger"]:
            warnings.append("""Webfinger result does not match actor URI""")

        return await render_template(
            "verify_actor_result.html.j2",
            messages=json.dumps(message.response, indent=2),
            result={key: value for key, value in result.items() if key != "webfinger"},
            actor_uri=actor_uri,
            warnings=warnings,
            has_warnings=len(warnings) > 0,
        )

    @app.get("/static/styles.css")
    async def stylesheet():
        return await render_template("styles.css"), 200, {"content-type": "text/css"}

    @app.get("/static/icon.svg")
    async def icon():
        return (
            await render_template("FediverseLogo.svg"),
            200,
            {"content-type": "image/svg+xml"},
        )

    @app.get("/")
    async def index():
        actor_uri = request.args.get("actor_uri")

        if actor_uri:
            actor_uri = actor_uri.strip()
            return await result_for_actor_uri(actor_uri)

        return await render_template("index.html.j2")

    @app.post("/")
    async def verify():
        form_data = await request.form
        actor_uri = form_data.get("actor_uri").strip()

        return await result_for_actor_uri(actor_uri)

    return app


@click.command()
@click.option("--only_generate_config", default=False, is_flag=True)
@click.option("--reload", default=False, is_flag=True)
@click.option(
    "--https",
    default=False,
    is_flag=True,
    help="Flag indicates that the server runs behind https",
)
@click.option("--port", default=2909, help="port to run on")
@click.option(
    "--domain", default="localhost:2909", help="domain the service is running on"
)
def verify_actor(only_generate_config, reload, https, port, domain):
    app = build_app(only_generate_config, domain, https)
    app.run(port=port, host="0.0.0.0", use_reloader=reload)


if __name__ == "__main__":
    verify_actor()
