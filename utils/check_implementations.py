# utils/check_implementations.py

import importlib, inspect, pkgutil
from pathlib import Path
from typing import Iterable, Mapping, Type

from contracts.data_types import (
    Data,
    DataCore,
)
from contracts.data_processors import (
    DataProcessor,
    DataProcessorCore,
)
from contracts.device_worker import (
    DeviceWorker,
    DeviceWorkerCore,
)
from contracts.plotter import Plotter
from utils.errors.errors import ImplementationError


def check_implementations() -> None:
    """Run all checks on the `implementations` package."""
    _, impl_root = _require_implementations_package()
    _check_directory_structure(impl_root)
    modules = _import_impl_modules()
    _check_contract_implementations(modules)
    _check_device_ui_files(impl_root, modules["devices_workers"])
    _check_config_file(impl_root)


# --------------------------------------------------------------------------- #
# Base package checks
# --------------------------------------------------------------------------- #

def _require_implementations_package():
    """Import `implementations` and return (module, root_path)."""
    try:
        pkg = importlib.import_module("implementations")
    except ImportError as exc:
        raise ImportError(
            "Could not import the 'implementations' package.\n"
            "Make sure an 'implementations/' folder is available on PYTHONPATH\n"
            "and contains an '__init__.py' file.\n\n"
            "A reference repository is available at:\n"
            "  https://github.com/Allyson-Robert/X-LAB_Plotting_Manager_Implementations"
        ) from exc

    # __file__ should be created by the interpreter, if not something is wrong
    file = getattr(pkg, "__file__", None)
    if not file:
        raise ImplementationError(
            "The 'implementations' package does not have a filesystem location."
        )

    return pkg, Path(file).resolve().parent


def _check_directory_structure(impl_root: Path) -> None:
    """Check that the expected directory layout is present."""
    # top-level dirs
    expected_dirs = [
        impl_root / "data",
        impl_root / "devices",
        impl_root / "plotters",
    ]
    missing_dirs = [d for d in expected_dirs if not d.exists()]
    if missing_dirs:
        raise FileNotFoundError(
            "The 'implementations' directory is missing required folders:\n"
            + "\n".join(f"  • {d}" for d in missing_dirs)
        )

    # check nested files and directories
    required_paths = [
        impl_root / "data" / "__init__.py",
        impl_root / "data" / "data_types" / "__init__.py",
        impl_root / "data" / "data_processors" / "__init__.py",
        impl_root / "devices" / "__init__.py",
        impl_root / "devices" / "workers" / "__init__.py",
        impl_root / "devices" / "widgets",
        impl_root / "plotters" / "__init__.py",
    ]
    missing = [p for p in required_paths if not p.exists()]
    if missing:
        lines = ["The 'implementations' directory is missing required files/directories:"]
        lines.extend(f"  • {p}" for p in missing)
        raise FileNotFoundError("\n".join(lines))


# --------------------------------------------------------------------------- #
# Imports and contract discovery
# --------------------------------------------------------------------------- #

class ImplementationImportError(RuntimeError):
    def __init__(self, base_pkg, errors):
        self.base_pkg = base_pkg
        self.errors = errors
        lines = [f"Failed to import some modules under {base_pkg.__name__}:"]
        for name, exc in errors.items():
            lines.append(f"  - {name}: {exc!r}")
        super().__init__("\n".join(lines))

def _import_impl_modules() -> Mapping[str, object]:
    """Import key implementation packages."""
    names = {
        "data_types": "implementations.data.data_types",
        "data_processors": "implementations.data.data_processors",
        "devices_workers": "implementations.devices.workers",
        "plotters": "implementations.plotters",
    }
    modules: dict[str, object] = {}
    for key, dotted in names.items():
        try:
            modules[key] = importlib.import_module(dotted)
        except ImportError as exc:
            raise ImportError(
                f"Could not import '{dotted}'.\n"
                "Check that the module/package exists and does not raise "
                "errors on import."
            ) from exc
    return modules

def _iter_package_modules(pkg, import_errors=None):
    """Yield a package and all its submodules, recording import errors."""
    if import_errors is None:
        import_errors = {}
    yield pkg
    pkg_path = getattr(pkg, "__path__", None)
    if pkg_path is None:
        return
    prefix = pkg.__name__ + "."
    for info in pkgutil.walk_packages(pkg_path, prefix):
        try:
            submod = importlib.import_module(info.name)
        except Exception as e:  # not just ImportError
            import_errors[info.name] = e
            continue
        else:
            yield submod

def _find_concrete_subclasses_in_package(
    pkg: object,
    base_classes: Iterable[Type[object]],
) -> list[Type[object]]:
    """Return all non-abstract subclasses of base_classes found in a package."""
    bases = tuple(base_classes)
    found: list[Type[object]] = []

    for module in _iter_package_modules(pkg):
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if not any(issubclass(cls, b) for b in bases):
                continue
            if cls in bases:
                continue
            if inspect.isabstract(cls):
                continue
            found.append(cls)

    return found


# --------------------------------------------------------------------------- #
# Contract checks
# --------------------------------------------------------------------------- #

def _check_contract_implementations(modules: Mapping[str, object]) -> None:
    """Ensure that each core contract has at least one implementation."""
    specs = [
        {
            "key": "data_types",
            "label": "data types",
            "bases": (Data, DataCore),
            "hint": (
                "Define at least one class that subclasses `Data` or `DataCore` "
                "and implements the required methods (e.g. read_file)."
            ),
        },
        {
            "key": "data_processors",
            "label": "data processors",
            "bases": (DataProcessor, DataProcessorCore),
            "hint": (
                "Define at least one class that subclasses `DataProcessor` or "
                "`DataProcessorCore` and performs the desired processing."
            ),
        },
        {
            "key": "devices_workers",
            "label": "device workers",
            "bases": (DeviceWorker, DeviceWorkerCore),
            "hint": (
                "Define at least one class that subclasses `DeviceWorker` or "
                "`DeviceWorkerCore` and implements the device control logic."
            ),
        },
        {
            "key": "plotters",
            "label": "plotters",
            "bases": (Plotter,),
            "hint": (
                "Define at least one class that subclasses `Plotter` and "
                "implements `ready_plot` and `draw_plot`."
            ),
        },
    ]

    for spec in specs:
        pkg = modules[spec["key"]]
        concrete = _find_concrete_subclasses_in_package(pkg, spec["bases"])
        if not concrete:
            raise ImplementationError(
                f"No concrete {spec['label']} found in {pkg.__name__}.\n"
                f"{spec['hint']}"
            )


# --------------------------------------------------------------------------- #
# Device ↔ UI checks
# --------------------------------------------------------------------------- #

def _check_device_ui_files(impl_root: Path, devices_pkg: object) -> None:
    """Check that each DeviceWorker has a matching .ui file."""
    widgets_dir = impl_root / "devices" / "widgets"
    if not widgets_dir.exists():
        raise FileNotFoundError(
            f"Widgets directory not found:\n  {widgets_dir}\n"
            "Create this directory and add a .ui file for each device."
        )

    devices = _find_concrete_subclasses_in_package(
        devices_pkg, base_classes=(DeviceWorker, DeviceWorkerCore)
    )

    missing: dict[str, Path] = {}
    for cls in devices:
        ui_name = getattr(cls, "ui_filename", None)
        if not ui_name:
            ui_name = f"{cls.__name__.lower()}.ui"
        ui_path = widgets_dir / ui_name
        if not ui_path.exists():
            missing[f"{cls.__module__}.{cls.__name__}"] = ui_path

    if missing:
        lines = [
            "Missing Qt .ui files for the following device workers:",
            *(f"  • {cls}  →  {path}" for cls, path in missing.items()),
            "",
            "Either create these .ui files in the widgets directory or set a "
            "`ui_filename` class attribute on each DeviceWorker to point to "
            "the correct file name.",
        ]
        raise FileNotFoundError("\n".join(lines))

def _check_config_file(impl_root: Path) -> None:
    """Check that the config.json file exists in the implementations root."""
    config_path = impl_root / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found:\n  {config_path}\n"
            "Create this file to define default settings for the implementations."
        )
