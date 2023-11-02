from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from grpc_reflection.v1alpha import reflection
from loguru import logger

from fsai_shared_funcs.proto_helpers.json_format import MessageToDict

# Example service_configs
# service_configs = {
#     "AreaOfInterestApi": {
#         "pb_definition": area_of_interest_api_pb2,
#         "grpc_definition": area_of_interest_api_pb2_grpc,
#         "servicer_instance": AreaOfInterestApi(db_pool),
#     }
# }


class ServiceConfig:
    def __init__(self, server, service_configs):
        self.server = server
        self.service_configs = service_configs

        # Add each servicer to the server
        for service_name, config in self.service_configs.items():
            grpc_definition = config["grpc_definition"]
            servicer_instance = config["servicer_instance"]

            # Get the appropriate add_*Servicer_to_server function
            add_servicer_func = getattr(
                grpc_definition, f"add_{service_name}Servicer_to_server"
            )

            # Add the servicer instance to the server
            add_servicer_func(servicer_instance, self.server)

            logger.info(f"Added {service_name} to server")

    def enable_reflection(self):
        # For each pb_definition in service_configs, add it to the server reflection
        SERVICE_NAMES = tuple(
            [
                self.service_configs[service]["pb_definition"]
                .DESCRIPTOR.services_by_name[service]
                .full_name
                for service in self.service_configs
            ]
        )

        reflection.enable_server_reflection(SERVICE_NAMES, self.server)

        logger.info("Enabled server reflection")


def get_grpc_data(stub_api, request_data=None, type="proto"):
    if request_data == None:
        # Setup the request
        request_data = google_dot_protobuf_dot_empty__pb2.Empty()

    # Wait for a response
    response = stub_api(request_data)

    logger.debug("Starting grpc api stream request.")

    if type == "proto":
        return response
    elif type == "dict":
        return MessageToDict(
            response,
            including_default_value_fields=True,
            preserving_proto_field_name=True,
            float_precision=14,
        )
    else:
        raise ValueError(f"Unknown type {type}")


def get_grpc_data_stream(stub_api, request=None, type="proto"):
    if request == None:
        # Setup the request
        request = google_dot_protobuf_dot_empty__pb2.Empty()

    # Wait for a response
    response = stub_api(request)

    logger.debug("Starting grpc api stream request.")

    for res in response:
        if type == "proto":
            yield res
        elif type == "dict":
            yield MessageToDict(
                res,
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                float_precision=14,
            )
        else:
            raise ValueError(f"Unknown type {type}")
