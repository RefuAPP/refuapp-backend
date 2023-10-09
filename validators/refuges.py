def validate_name(name: str) -> str:
    if not name.strip(' ')[0].istitle():
        raise ValueError('name must start with a capital letter')
    return name


def validate_region(region: str) -> str:
    if not region.istitle():
        raise ValueError('region must be capitalized')
    return region
