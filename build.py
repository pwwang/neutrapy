from setuptools_rust import Binding, RustExtension


def build(setup_kwargs):
    setup_kwargs.update({
        "rust_extensions": [
            RustExtension('neutrapy.current_platform_rs', binding=Binding.PyO3)
        ],
    })
