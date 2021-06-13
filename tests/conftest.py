from pathlib import Path
import pytest
import yaml

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shopping_cart import data_model as m
from shopping_cart.store.operations import populate


directory = Path(__file__).parent


@pytest.fixture(name="session")
def make_session():
    engine = create_engine('sqlite://')
    session = sessionmaker(bind=engine)()
    m.Base.metadata.create_all(engine)
    yield session
    session.close()


@pytest.fixture(name="product")
def make_product():
    """
    Pytest fixture to generate a product instance

    """

    def _generate(
            product_id: int,
            name: str,
            price: float
    ):
        return m.Product(
            id=product_id,
            name=name,
            unit_price=price
        )

    return _generate


@pytest.fixture(name="store")
def make_store_database(session):
    """
    Pytest fixture to add list of products
    to the store database from a mock store configuration

    """

    with open(directory / "mock_data/store.yaml") as f:
        model_dict = yaml.safe_load(f)

    populate(
        model_dict,
        session
    )

    return session



#
#
#
# @pytest.fixture(name="role_nurse")
# def make_role_nurse():
#     return Role(name="nurse")
#
#
# @pytest.fixture(name="role_odp")
# def make_odp():
#     return Role(name="ODP")
#
#
# @pytest.fixture(
#     autouse=True
# )
# def add_roles(
#         role_surgeon,
#         role_nurse,
#         role_odp,
#         session
# ):
#     session.add(role_surgeon)
#     session.add(role_nurse)
#     session.add(role_odp)
#
#
# @pytest.fixture(name="field_textual")
# def make_field_textual():
#     return model.TextualField(
#         id="textual_key"
#     )
#
#
# @pytest.fixture(name="question_numerical")
# def make_field_numerical(
#         session,
#         field_numerical
# ):
#     return model.Question(
#         name="numerical_title",
#         field=field_numerical
#     )
#
#
# @pytest.fixture(name="field_numerical")
# def make_field_numerical():
#     return model.NumericalField(
#         id="numerical_key"
#     )
#
#
# @pytest.fixture(name="field_confirmation")
# def make_field_confirmation():
#     return model.ConfirmationField(
#         id="confirmation_key"
#     )
#
#
# @pytest.fixture(name="patient")
# def make_patient(operation):
#     patient = model.Patient(
#         id="1234",
#         operations=[operation],
#         admission_timestamp=dt.datetime(2017, 8, 30),
#         date_of_birth=dt.date.today() - dt.timedelta(
#             days=55 * 365.25 + 1),
#         sex="m",
#         name="jenny"
#     )
#
#     patient.data_dict = {}
#
#     return patient
#
#
# @pytest.fixture(
#     name="procedure_type"
# )
# def make_procedure_type():
#     return model.ProcedureType(
#         name="Hemicolectomy",
#         opcs_code="H07.1"
#     )
#
#
# @pytest.fixture(
#     name="position"
# )
# def make_position():
#     return model.Position(
#         name="Supine"
#     )
#
#
# @pytest.fixture(name="procedure")
# def make_procedure(
#         procedure_type
# ):
#     return model.Procedure(
#         procedure_type=procedure_type,
#         surgical_site="Right"
#     )
#
#
# @pytest.fixture(
#     name="operation",
#     autouse=True
# )
# def make_operation(
#         procedure,
#         position
# ):
#     operation = model.Operation(
#         id=1,
#         scheduled_datetime=dt.datetime(2017, 9, 4, 11, 30),
#         procedures=[procedure],
#         expected_duration=120,
#         positions=[position]
#     )
#     procedure.operation = operation
#     return operation
#
#
