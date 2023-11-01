import builtins
import importlib
import importlib.metadata as importlib_metadata
import logging
import pkgutil
from collections import defaultdict
from types import ModuleType
from typing import Any, Callable, Dict, List, Literal, Optional, Union

AVAILABLE_ENTRY_POINTS = None

logger = logging.getLogger(__name__)


class RecipeLoadError(Exception):
    pass


class RecipePackageNotFound(RecipeLoadError):
    def __init__(self, package_name: str):
        self.package_name = package_name
        super().__init__(f"Could not find recipe package '{package_name}'")


class RecipeImportError(RecipeLoadError):
    def __init__(self, package_name: str, failed_imports: List[str]):
        self.package_name = package_name
        self.failed_imports = failed_imports
        super().__init__(
            f"Errors while importing '{package_name}' (modules: {failed_imports})"
        )


class RecipeSyntaxError(RecipeLoadError):
    def __init__(self, package_name: str):
        self.package_name = package_name
        super().__init__(f"Recipe package '{package_name}' contains syntax error)")


class RecipeLoader:
    """
    Handles discovery and recursive imports of recipe packages on demand.
    """

    def __init__(
        self,
    ):
        # The entrypoint namespace we search for to discover installed
        # recipe packages in the local environment.
        self._entry_point_namespace = "prodigy_teams_recipes"
        # When _loaded[package] is True, all recipes under that namespace
        # are imported. Contains both top-level packages and modules.
        self._loaded = {}
        # _known_import_paths[package] specifies an optional subset of modules
        # containing recipes. Custom recipe packages can specify these through
        # a list of entrypoints under self._entry_point_namespace
        self._known_import_paths: Dict[str, List[str]] = {}

    def register_import_path(
        self, package: str, entrypoints: List[importlib_metadata.EntryPoint]
    ):
        def sorted_unique_modules(entrypoints):
            # For now, only consider the module names of the entrypoints.
            # Since we may be able to enumerate recipes individually in
            # the future, this this ensures compatibility with newer
            # recipe packages.
            return list(sorted(builtins.set([e.module for e in entrypoints])))

        self._known_import_paths[package] = sorted_unique_modules(entrypoints)

    def discover_packages_from_entrypoints(self) -> List[str]:
        """
        Find all installed packages that specify a recipe entrypoint.

        Returns the top level recipe package and caches the specified
        submodule paths containing recipes.
        """
        discovered = self._discover_entrypoints()
        for package_name, entrypoints in discovered.items():
            self.register_import_path(package_name, entrypoints)

        logger.debug(
            "Discovered %s packages from entrypoints: %s",
            len(discovered),
            list(discovered.keys()),
        )
        return list(discovered.keys())

    def _discover_entrypoints(self) -> Dict[str, List[importlib_metadata.EntryPoint]]:
        """
        Gets all raw entrypoints in the `prodigy_teams_recipes` namespace from the current venv
        """
        # Entrypoint scans are expensive, so we only do the environment scan once.
        global AVAILABLE_ENTRY_POINTS

        by_package = defaultdict(list)
        if AVAILABLE_ENTRY_POINTS is None:
            AVAILABLE_ENTRY_POINTS = importlib_metadata.entry_points()

        for entrypoint in AVAILABLE_ENTRY_POINTS.get(self._entry_point_namespace, []):
            package_name = entrypoint.module.split(".")[0]
            by_package[package_name].append(entrypoint)
        return dict(by_package)

    def _get_entrypoints(
        self, package_name: str
    ) -> Optional[List[importlib_metadata.EntryPoint]]:
        """
        Gets all entrypoints for a given package name
        """
        try:
            distribution = importlib_metadata.Distribution.from_name(package_name)
            return distribution.entry_points
        except importlib_metadata.PackageNotFoundError:
            logger.debug("No Distribution found for '%s'", package_name)
            return None

    def load_recursive(
        self,
        root: ModuleType,
        on_error: Union[
            Literal["skip", "raise"], Callable[[str, Exception], Any]
        ] = "raise",
    ):
        """
        Import all recipes from a root recipes module (e.g. `prodigy_teams_recipes.recipes`)
        """

        results = {}

        def _load_module(name: str):
            try:
                module = importlib.import_module(name)
                return module
            except Exception as e:
                if on_error == "skip":
                    logger.debug("Error importing submodule '%s'. Skipping...", name)
                    return
                elif callable(on_error):
                    on_error(name, e)
                else:
                    assert on_error == "raise"
                    raise

        for _, subname, is_pkg in pkgutil.iter_modules(
            root.__path__, prefix=root.__name__ + "."
        ):
            if subname in results:
                continue
            else:
                logger.debug(
                    "Importing module '%s'",
                    subname,
                )
            submodule = _load_module(subname)
            if is_pkg and submodule is not None:
                results.update(self.load_recursive(submodule, on_error))
            results[subname] = submodule
        results[root.__name__] = root

        return results

    def load_package(
        self,
        package: Union[str, ModuleType],
        must_exist: bool = True,
        skip_errors: bool = False,
    ):
        """
        Import all recipes from a package (e.g. `prodigy_teams_recipes`)
        """
        package_name = package if isinstance(package, str) else package.__name__  # type: ignore
        if self._loaded.get(package_name, False):
            # We only set _loaded for successful imports for now
            # since errors may be handled differently by each caller.
            logger.debug("Skipping '%s': already loaded", package_name)
            return self._loaded[package_name]

        logger.info("Loading recipes from '%s'", package_name)
        entrypoints = self._get_entrypoints(package_name)
        if entrypoints is not None:
            logger.debug(
                "discovered entrypoints for '%s': '%s'", package_name, entrypoints
            )
            self.register_import_path(package_name, entrypoints)

        root_modules = []
        root_imports = self._known_import_paths.get(package_name, [])
        if isinstance(package, ModuleType):
            root_modules.append(package)
        elif not root_imports:
            # if we don't know any import paths, import `package` recursively
            root_imports.append(".")

        if skip_errors:
            on_error = "skip"
        else:
            on_error = "raise"

        # Get our root packages, since if these are missing that's a serious error
        for import_path in root_imports:
            try:
                root_modules.append(
                    importlib.import_module(import_path, package=package_name)
                )
            except ModuleNotFoundError as e:
                assert e.name is not None
                if e.name != package_name:
                    # Indicates the package was found, but it tried to import something else which failed
                    raise RecipeImportError(package_name, [e.name]) from e
                if must_exist:
                    raise RecipePackageNotFound(package_name) from e
                else:
                    continue
            except Exception as e:
                # Indicates the package was found, but something else failed during import
                # of the top level package (e.g. missing dependency, syntax errors)
                raise RecipeImportError(package_name, []) from e
        currently_importing = None
        try:
            for root in root_modules:
                currently_importing = root.__name__

                loaded = self.load_recursive(root, on_error=on_error)
                self._loaded.update({k: True for k in loaded.keys()})
        except Exception as e:
            raise RecipeImportError(
                package_name, [currently_importing or package_name]
            ) from e
        logger.debug("Loaded recipes from package: %s", package_name)
        return self._loaded.get(package_name, False)

    @property
    def builtin_recipes_package(self) -> str:
        """Returns the root package name for the built-in recipes"""
        return "prodigy_teams_recipes"
