import os
import sys
from pyschemavalidator import FastAPIErrorSchema

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


if __name__ == "__main__":
    # Example usage of the FastAPIErrorSchema class.
    err = FastAPIErrorSchema.validation_error(
        loc=["request", "body"],
        input={'data_path': 'test'},
    )
    print(err.to_dict())
