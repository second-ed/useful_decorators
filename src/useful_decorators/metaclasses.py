class SingletonMeta(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):  # type: ignore[no-untyped-def]
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
