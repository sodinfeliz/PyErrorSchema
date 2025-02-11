import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pyerrorschema import ErrorSchema, FastAPIErrorSchema

if __name__ == "__main__":

    err1 = ErrorSchema.database_error(
        msg="Database connection failed."
    )

    err2 = FastAPIErrorSchema.customized_error(
        type="customized_error",
        msg="Customized error.",
        loc=["request"],
        input={'test': 'test'},
    )

    # Single error schema to string
    print(err1.to_dict())
