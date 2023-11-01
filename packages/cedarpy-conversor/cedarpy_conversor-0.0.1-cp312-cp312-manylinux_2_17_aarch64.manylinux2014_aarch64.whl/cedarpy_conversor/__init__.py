from cedarpy_conversor import _internal

def echo(s: str) -> str:
    return _internal.echo(s)

def convert_json_to_cedar_policies(policies: str) -> str:
    """Convert the provided policies from JSON to Cedar Policy.

    :param policies is a str containing the policies to be converted

    :returns the converted policy
    :raises ValueError: if the input policies cannot be parsed
    """
    return _internal.convert_json_to_cedar_policies(policies)


def convert_cedar_policies_to_json(policies: str) -> str:
    """Convert the provided policies from Cedar Policy to JSON.

    :param policies is a str containing the policies to be converted

    :returns the converted policy
    :raises ValueError: if the input policies cannot be parsed
    """
    return _internal.convert_cedar_policies_to_json(policies)