class Fillable:

    def __init__(self, inputs: dict[str, str] | None = None) -> None:

        if inputs is not None:
            self.fill(inputs)

    def fill(self, inputs: dict[str, str]) -> 'Fillable':

        for key, value in inputs.items():
            if self.__isset(key):
                setattr(self, key, value)
        return self

    def __isset(self, name: str) -> bool:

        return hasattr(self, name)

    def __getattr__(self, name: str) -> str:

        if self.__isset(name):
            return getattr(self, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name: str, value: str) -> None:

        super().__setattr__(name, value)
