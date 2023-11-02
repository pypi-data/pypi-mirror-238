from linker_atom.api.base import UdfAPIRoute
from linker_atom.api.schema.response import Heartbeat

healthcheck_route = UdfAPIRoute()


@healthcheck_route.get("/v1/health/ping", response_model=Heartbeat, name="ping")
async def ping() -> Heartbeat:
    heartbeat = Heartbeat(is_alive=True)
    return heartbeat
