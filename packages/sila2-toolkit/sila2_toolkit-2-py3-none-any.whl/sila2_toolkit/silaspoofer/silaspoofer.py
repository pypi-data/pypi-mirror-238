""" sila_defs = ["Fluent.sila.xml", "shakecontroller.sila.xml"]
server_name = "FluentServer"
server_uuid = "123e4567-e89b-12d3-a456-426655440000"
port = 50053
address = "127.0.0.1"
insecure = True """

from dataclasses import dataclass
from typing import Any
from sila2.server import SilaServer, FeatureImplementationBase
from sila2.framework import Feature



class DummyServer(SilaServer):
    """A dummy server that implements the given SiLA definitions.

    Args:
        sila_defs (list[str]): List of SiLA definitions to be simulated.
        server_name (str): The name of the server.
        server_uuid (str): The unique identifier of the server.

    Attributes:
        implementation (dict): Dictionary containing the mock implementations of the features.

    """

    def __init__(
        self,
        sila_defs: list[str],
        server_name: str,
        server_uuid: str,
        overrides: dict[str, dict],
    ):
        """Initializes the dummy server.

        Args:
            sila_defs (list[str]): List of SiLA definitions to be simulated.
            server_name (str): The name of the server.
            server_uuid (str): The unique identifier of the server.
        """
        super().__init__(
            server_name=server_name,
            server_type=server_name,
            server_version="1.0",
            server_description="This is a dummy server",
            server_vendor_url="http://dummy",
            server_uuid=server_uuid,
        )

        self.implementation = {}
        self.feature_lookup = {}

        for sila_def in sila_defs:
            feature = Feature(sila_def)
            spoof = SpoofImplementation(feature)(self)

            self.implementation[feature.fully_qualified_identifier] = spoof
            self.feature_lookup[sila_def] = spoof
       

            if sila_def in overrides:
                override = overrides[sila_def]
        

                @dataclass
                class DataCall:
                    value: Any

                    def __call__(self, *args: Any, **kwargs: Any) -> Any:
                    
                        return eval(self.value, None, None)

                for k, v in override.items():
                    setattr(self.feature_lookup[sila_def], k, DataCall(v))

            self.set_feature_implementation(
                feature, self.implementation[feature.fully_qualified_identifier]
            )


def SpoofImplementation(feature: Feature):
    """Creates a mock implementation for the given feature.

    Args:
        feature (Feature): The feature to be mocked.

    Returns:


    """

    def MakeMock(name):
        """Creates a mock function...

        Args:
            name (Any):

        Returns:

        """

        def Mock(*args, **kwargs):
            """Prints the given arguments.

            Args:
                *args (Any):
                **kwargs (Any):

            """
            print(f"Mocking '{name}': {args} {kwargs}")

        return Mock

    calls = {
        k: MakeMock(k)
        for k, v in (
            feature._observable_commands | feature._unobservable_commands
        ).items()
    }

    properties = {
        f"get_{k}": MakeMock(k)
        for k, v in (
            feature._observable_properties | feature._unobservable_properties
        ).items()
    }

    # cmd = feature._observable_commands["Start"]
    # ptype = cmd.parameters.namedtuple_type
    # print(ptype(Name="", ExternalScripts=[], VariableReplacements=[]))
    # print(cmd.parameters.message_type)

    Impl = type(
        f"{feature._identifier}",
        (FeatureImplementationBase,),
        calls | properties,
    )

    Impl.__init__ = lambda self, server: super(Impl, self).__init__(server)
    return Impl


def StartServer(
    sila_defs: list[str],
    name: str,
    uuid: str,
    port: int,
    address: str = "127.0.0.1",
    overrides={},
) -> DummyServer:
    """Starts a dummy server with the given configuration.

    Args:
        sila_defs (list[str]): List of SiLA definitions to be simulated.
        name (str): The name of the server.
        uuid (str): The unique identifier of the server.
        port (int): The port to be used for the server.
        address (str, optional): The address to be used for the server. Defaults to "127.0.0.1".

    Returns:
        DummyServer: The started server.
    """

    server = DummyServer(sila_defs, name, uuid, overrides)

    server.start_insecure(
        address=address,
        port=port,
    )

    return server


def StartServers(config: list):
    """
    Args:
        config (list) : List of dictionaries containing the configuration for the servers to be started.
    Returns:
        list : List of started servers.
    """
    return [StartServer(**i) for i in config]




