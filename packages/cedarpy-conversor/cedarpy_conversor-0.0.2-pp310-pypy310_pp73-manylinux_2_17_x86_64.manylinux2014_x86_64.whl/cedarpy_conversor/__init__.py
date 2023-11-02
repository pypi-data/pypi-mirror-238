from cedarpy_conversor import _internal

def echo(s: str) -> str:
    return _internal.echo(s)

def convert_json_to_cedar_policies(policies_json_representation: str) -> str:
    """Convert the provided policies JSON representation to Cedar Policy.

    Parameters
    ----------
        * policies_json_representation: is a str containing the policies json representation to be converted

    Returns
    -------
        The converted policies (str)
        
    Raises
    -------
        ValueError: if the input policies_json_representation cannot be parsed or are not valid
    
    Examples
    -------
        ```python
        from cedarpy_conversor import convert_json_to_cedar_policies
        
        def main():
            json_representation_policies = "..."
            policies = convert_json_to_cedar_policies(json_representation_policies)
            print(policies)
        ```
    """
    return _internal.convert_json_to_cedar_policies(policies_json_representation)


def convert_cedar_policies_to_json(policies: str) -> str:
    """Convert the provided policies from Cedar Policy to JSON representation.

    Parameters
    ----------
        * policies: is a str containing the policies to be converted

    Returns
    -------
        The JSON representation of the policies (str)
        
    Raises
    -------
        ValueError: if the input policies cannot be parsed or are not valid
    
    Examples
    -------
        ```python
        from cedarpy_conversor import convert_cedar_policies_to_json
        
        def main():
            policies = "..."
            json_policies = convert_cedar_policies_to_json(policies)
            print(json_policies)
        ```
    """
    return _internal.convert_cedar_policies_to_json(policies)


class EntityTypeAndName:
   
    def __init__(self, response: dict):
        self._entity_type = response['entity_type']
        self._entity_id = response['entity_id']
    
    @property
    def entity_type(self) -> str:
        return self._entity_type
    
    @property
    def entity_id(self) -> str:
        return self._entity_id
    
    @property
    def __dict__(self):
        return {
            'entity_type': self.entity_type,
            'entity_id': self.entity_id
        }
    
def get_entity_type_and_id(entity: str) -> EntityTypeAndName:
    """Get the entity type and id from the provided entity.

    Parameters
    ----------
        * entity: is a str containing the entity to be parsed

    Returns
    -------
        The entity type and id (str)
        
    Raises
    -------
        ValueError: if the input entity cannot be parsed or are not valid
    
    Examples
    -------
        ```python
        from cedarpy_conversor import get_entity_type_and_id
        
        def main():
            entity = "..."
            entity_type_and_name = get_entity_type_and_id(entity)
            print(entity_type_and_name)
        ```
    """
    return EntityTypeAndName(_internal.get_entity_type_and_id(entity))