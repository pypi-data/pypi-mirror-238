from typing import Callable, List, Tuple, Iterator, TYPE_CHECKING

if TYPE_CHECKING:
    from .Application import Application
    from ..request import Request
    from ..response import Response

ResponseHandler = Callable[[str, List[Tuple]], None]


def response_handler(environ: dict, start_response: ResponseHandler) -> Iterator:
    """The WSGI Application Server.

    Arguments:
        environ {dict} -- The WSGI environ dictionary
        start_response {WSGI callable}

    Returns:
        WSGI Response
    """
    from wsgi import application

    application.bind("environ", environ)

    """Add Environ To Service Container
    Add the environ to the service container. The environ is generated by the
    the WSGI server above and used by a service provider to manipulate the
    incoming requests
    """

    # """Execute All Service Providers That Require The WSGI Server
    # Run all service provider boot methods if the wsgi attribute is true.
    # """

    try:
        for provider in application.get_providers():
            application.resolve(provider.boot)
    except Exception as e:
        application.make("exception_handler").handle(e)

    """We Are Ready For Launch
    If we have a solid response and not redirecting then we need to return
    a 200 status code along with the data. If we don't, then we'll have
    to return a 302 redirection to where ever the user would like go
    to next.
    """
    _ = application.make("request")
    response: "Response" = application.make("response")

    start_response(
        response.get_status_code(),
        response.get_headers() + response.cookie_jar.render_response(),
    )

    """Final Step
    This will take the data variable from the Service Container and return
    it to the WSGI server.
    """
    return iter([response.get_response_content()])


def testcase_handler(
    application: "Application",
    environ: dict,
    start_response: ResponseHandler,
    exception_handling: bool = True,
) -> Tuple["Request", "Response"]:
    """The WSGI Application Server."""
    from wsgi import application

    application.bind("environ", environ)

    """Add Environ To Service Container
    Add the environ to the service container. The environ is generated by the
    the WSGI server above and used by a service provider to manipulate the
    incoming requests
    """

    # """Execute All Service Providers That Require The WSGI Server
    # Run all service provider boot methods if the wsgi attribute is true.
    # """

    try:
        for provider in application.get_providers():
            application.resolve(provider.boot)
    except Exception as e:
        if not exception_handling:
            raise e
        application.make("exception_handler").handle(e)

    """We Are Ready For Launch
    If we have a solid response and not redirecting then we need to return
    a 200 status code along with the data. If we don't, then we'll have
    to return a 302 redirection to where ever the user would like go
    to next.
    """

    request, response = application.make("request"), application.make("response")

    start_response(
        response.get_status_code(),
        response.get_headers() + response.cookie_jar.render_response(),
    )

    """Final Step
    This will take the data variable from the Service Container and return
    it to the WSGI server.
    """
    return (request, response)
