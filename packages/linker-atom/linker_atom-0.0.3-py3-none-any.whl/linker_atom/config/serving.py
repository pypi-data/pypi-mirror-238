import socket
from typing import List

from pydantic import BaseModel, Field


class ServingConfig(BaseModel):
    serving_host: str = Field(alias="servingHost", default="")
    serving_port: int = Field(alias="servingPort", default=80)
    ability_code: str = Field(alias="abilityCode", default="")
    atom_code: str = Field(alias="atomCode", default="")
    host_node_name: str = Field(env="HOST_NODE_NAME", default="")
    ability_code_instance: str = Field(alias="abilityCodeInstance", default="")
    ability_depend_atom_codes: List[str] = Field(alias="abilityDependAtomCodes", default=[])
    model_ids: str = Field(alias="modelIds", default="")
    svc_address: str = Field(alias="svcAddress", default="")
    
    @property
    def serving_domain(self) -> str:
        if self.serving_host:
            return f"http://{self.serving_host}:{self.serving_port}"
        if self.host_node_name:
            return f"http://{self.host_node_name}:{self.serving_port}"
        return f"http://{socket.gethostname()}:{self.serving_port}"
