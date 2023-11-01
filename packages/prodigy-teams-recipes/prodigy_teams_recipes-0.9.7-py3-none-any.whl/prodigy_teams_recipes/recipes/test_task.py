import time
from typing import List, Optional

import fastapi
from prodigy.types import RecipeSettingsType, TaskType
from prodigy_teams_recipes_sdk import BoolProps, FloatProps, IntProps, task_recipe
from pydantic import BaseModel


@task_recipe(
    title="Test Task",
    description="Task with tunable delays and errors for testing.",
    view_id="text",
    field_props={
        "startup_delay_s": FloatProps(
            title="Startup delay",
            description="Number of seconds to sleep before starting the server.",
            min=0.0,
            step=1.0,
        ),
        "healthcheck_delay_s": FloatProps(
            title="Healthcheck delay",
            description=(
                "Number of seconds to delay `/version`, `/health`, `/healthz` endpoints after server start (returns HTTP 503)."
            ),
            min=0.0,
            step=1.0,
        ),
        "num_examples": IntProps(title="Number of examples", min=0),
        "crash_on_startup": BoolProps(
            title="Crash on startup",
            description="If true, crashes before starting server (after startup_delay_s)",
        ),
        "healthcheck_error": BoolProps(
            title="Healthcheck error",
            description="Returns an error from `/version`, `/health`, `/healthz` endpoints after server start (returns HTTP 500).",
        ),
        "crash_on_update": BoolProps(
            title="Crash on update",
            description="Crash when annotations are saved",
        ),
    },
)
def test_task(
    *,
    startup_delay_s: float = 0.0,
    healthcheck_delay_s: float = 0.0,
    num_examples: int = 100,
    crash_on_update: bool = False,
    crash_on_startup: bool = False,
    healthcheck_error: bool = False,
) -> RecipeSettingsType:
    """
    Can be configured to start slowly, crash on first annotation save, or fail
    healthchecks without crashing
    """
    assert startup_delay_s >= 0.0, "startup_delay_s must be >= 0.0"
    assert healthcheck_delay_s >= 0.0, "healthcheck_delay_s must be >= 0.0"
    started_at = time.time()
    # imports are inside the recipe to avoid side effects
    from prodigy.app import app
    from prodigy.app import get_health as base_health
    from prodigy.app import version as base_version

    stream = ({"text": f"Example {i} of {num_examples}"} for i in range(num_examples))

    healthcheck_params = {
        "/version": {
            "handler": base_version,
            "error_code": 500 if healthcheck_error else None,
        },
        "/health": {
            "handler": base_health,
            "error_code": 500 if healthcheck_error else None,
        },
        "/healthz": {
            "handler": base_health,
            "error_code": 500 if healthcheck_error else None,
        },
    }
    router: fastapi.APIRouter = app.router
    app.router.routes = [
        route for route in router.routes if route.path_format not in healthcheck_params  # type: ignore
    ]

    def wrap(name):
        params = healthcheck_params[name]

        def _wrapped():
            if healthcheck_delay_s > 0.0:
                healthcheck_ready_at = (
                    started_at + startup_delay_s + healthcheck_delay_s
                )
                delay_remaining = healthcheck_ready_at - time.time()
                if delay_remaining > 0:
                    print(
                        f"Test task: delayed {name} returning 503 ({delay_remaining} seconds of delay remaining)"
                    )
                    # endpoints only become accessible after the recipe returns, so if we delay
                    # startup we need to also delay the healthcheck by the same amount
                    raise fastapi.HTTPException(
                        status_code=503, detail=f"Mocked {name} (always errors)"
                    )
            if params["error_code"] is not None:
                print(
                    f"Test task: {name} override returning {params['error_code']} error"
                )
                # return a 500 error
                raise fastapi.HTTPException(
                    status_code=params["error_code"],  # type: ignore
                    detail=f"Mocked {name} (always errors)",
                )
            return params["handler"]()

        return _wrapped

    class SetHealtcheck(BaseModel):
        endpoints: List[str] = ["/version", "/health", "/healthz"]
        error_code: Optional[int] = 500

    def set_healthcheck(body: SetHealtcheck):
        for endpoint in body.endpoints:
            healthcheck_params[endpoint]["error_code"] = body.error_code
        return {
            endpoint: params
            for endpoint, params in healthcheck_params.items()
            if endpoint in body.endpoints
        }

    app.router.add_api_route(
        "/set-healthcheck",
        set_healthcheck,
        tags=["api"],
        methods=["POST"],
    )
    for name in healthcheck_params:
        print(f"Test task: setting up endpoint overrides for {name}")
        app.router.add_api_route(
            name,
            wrap(name),
            tags=["override", "api"],
            methods=["GET"],
        )

    def make_update(_: List[TaskType]) -> None:
        if crash_on_update:
            raise Exception("Crashing on update")

    if startup_delay_s > 0.0:
        startup_ready_at = started_at + startup_delay_s
        delay_remaining = startup_ready_at - time.time()
        if delay_remaining > 0:
            print(f"Test task: startup delay sleeping {delay_remaining} seconds")
            time.sleep(delay_remaining)
        print("Test task: startup delay done")
    if crash_on_startup:
        raise Exception("Crashed after startup")
    return {
        "stream": stream,
        "dataset": False,
        "view_id": "text",
        "update": make_update,
    }
