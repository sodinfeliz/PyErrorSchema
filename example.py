from innodisk_error_schema import ErrorSchema, FastAPIErrorSchema


if __name__ == "__main__":
    # Example usage of the ErrorSchema and FastAPIErrorSchema classes.
    err = ErrorSchema.database_error()
    print(err.to_dict())

    err = FastAPIErrorSchema.validation_error(
        loc=["request", "body"],
        input={'data_path': 'test'},
    )
    print(err.to_dict())

