"""Custom data generation for specific variables."""


from faker import Faker


def generate_organisation_number(faker: Faker) -> str:
    """Generate a fake organisation number.

    Matches the format defined here: https://www.ssb.no/a/metadata/conceptvariable/vardok/1350/en
    """
    return str(faker.unique.random_number(digits=9, fix_len=True))
