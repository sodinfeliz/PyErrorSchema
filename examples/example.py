import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pyerrorschema import FastAPIErrorSchema


if __name__ == "__main__":
    # Example usage of the FastAPIErrorSchema class.
    err = FastAPIErrorSchema.database_error(
        loc=["request", "body"],
        input={'data_path': 'test'},
    )
    print(err.to_dict())

    err = FastAPIErrorSchema.customized_error(
        type="customized_error",
        msg="Customized error.",
        loc=["request"],
        input={'test': 'test'},
    )
    print(err.to_dict())
