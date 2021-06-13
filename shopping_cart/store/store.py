from copy import deepcopy

from sqlalchemy.orm import Session

import scalpel_model as m


def populate(
        model_dict: dict,
        session: Session
):
    """
    Parse data from YAML and add it to the database.
    """
    model_dict = deepcopy(model_dict)

    role_dicts = model_dict[
        "roles"
    ]

    for role_dict in role_dicts:
        if role_dict.get(
                "is_clinical"
        ) is not False and not m.Role.exists_with_name(
            role_dict["name"],
            session
        ):
            session.add(
                m.Role(
                    **role_dict
                )
            )

    user_dicts = model_dict[
        "users"
    ]

    for user_dict in user_dicts:
        role_name = user_dict["role"]
        if not m.Role.exists_with_name(
                role_name,
                session
        ):
            print(
                f"No clinical role found with name {role_name}"
            )
            continue
        role = m.Role.with_name(
            user_dict["role"],
            session
        )

        user_id = user_dict["id"]
        if m.Clinician.is_instance_with_id(
                user_id,
                session
        ):
            print(f"Clinician {user_id} already exists")
        else:
            user = m.Clinician(
                id=user_dict["id"],
                name=user_dict["name"],
                role=role,
                email=user_dict["email"]
            )
            session.add(
                user
            )

    session.commit()