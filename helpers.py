def checkbox_to_bool(checkbox_value: str) -> bool:
    if checkbox_value == 'on':
        return True
    else:
        return False


def create_where(args):
    initial = "WHERE ({});"

