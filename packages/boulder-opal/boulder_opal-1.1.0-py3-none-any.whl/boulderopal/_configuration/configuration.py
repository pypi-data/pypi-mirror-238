# Copyright 2023 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

from typing import Any

from qctrlworkflowclient import (
    ApiRouter,
    CoreClientSettings,
    LocalRouter,
    Product,
    get_authenticated_client_for_product,
    get_default_api_url,
    get_default_cli_auth,
)
from qctrlworkflowclient.globals import global_value

from boulderopal._configuration.constants import INVALID_SUBSCRIPTION_ERROR
from boulderopal._configuration.verbosity import MESSAGE_PRINTER


def get_default_router() -> ApiRouter:
    """
    Return the default router that the Boulder Opal client uses.
    """
    client = get_authenticated_client_for_product(
        product_access_required="boulder-opal-cli-access",
        api_url=get_default_api_url(),
        auth=get_default_cli_auth(),
        invalid_access_error_message=INVALID_SUBSCRIPTION_ERROR,
    )
    settings = get_configuration()

    return ApiRouter(client, settings)


@global_value("BOULDER_OPAL_CONFIGURATION")
def get_configuration() -> CoreClientSettings:
    """
    Return the global Boulder Opal settings.
    """
    return CoreClientSettings(
        router=get_default_router,
        product=Product.BOULDER_OPAL,
        event_listeners=[MESSAGE_PRINTER],
    )


def configure(**kwargs: Any) -> None:
    """
    Update the global Boulder Opal settings. See :class:`CoreClientSettings`
    for details on which fields can be updated.
    """
    configuration = get_configuration()
    configuration.update(**kwargs)


def set_local(resolver: "BaseResolver") -> None:  # type: ignore
    """
    Configure Boulder Opal for local routing.

    Parameters
    ----------
    resolver : BaseResolver
        A local implementation of a workflow resolver which uses
        a registry that implements all of the available Boulder Opal
        workflows.
    """
    configure(router=LocalRouter(resolver))


def in_local_mode() -> bool:
    """
    Check if client is in local mode.
    """
    return isinstance(get_configuration().get_router(), LocalRouter)


def is_async(result: Any) -> bool:
    """
    Check if we get async result back from the server.
    """
    return isinstance(result, dict) and result.get("async_result") is not None


def set_local_mode() -> None:
    """
    Set the Boulder Opal client to operate in local mode.

    Local mode requires a Boulder Opal Core installation.
    """
    try:
        from boulderopalcore.api import (  # pylint: disable=import-outside-toplevel
            SynchronousResolver,
            get_boulder_core_api,
        )

    except ImportError as exc:
        raise ImportError(
            "Cannot find a Boulder Opal Core installation. "
            "Contact us at https://q-ctrl.com/contact if you need assistance."
        ) from exc

    set_local(SynchronousResolver(get_boulder_core_api()))


def set_cloud_mode() -> None:
    """
    Set the Boulder Opal client to operate in cloud mode.
    """
    configure(router=get_default_router())
