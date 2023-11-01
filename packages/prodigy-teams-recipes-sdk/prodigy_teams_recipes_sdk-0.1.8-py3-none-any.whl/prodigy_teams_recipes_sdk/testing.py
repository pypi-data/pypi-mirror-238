import re
from pathlib import Path
from typing import Optional


class CustomRecipesPackage:
    def __init__(
        self,
        project_name: str,
        parent_dir: Path,
        package_name: Optional[str] = None,
        distribution_name: Optional[str] = None,
        version: str = "0.1.0",
    ):
        self.parent_dir = parent_dir
        # Python package names are extremely confusing. Here we use the following:
        # - project_name is the name of the directory containing the setup.py/pyproject.toml
        #   and can be chosen freely.
        # - package_name is the name used to import the package, e.g. `import package_name`
        #   and must be a valid python identifier.
        #   If unspecified, we derive it from the distribution_name (if specified) or project_name.
        # - distribution_name is the name of the package as it will be distributed on PyPI.
        #   This can be any mix of lower/uppercase letters, numbers, hyphens, or underscores
        #   and does not have to match the package_name. If unspecified, we derive it from
        #   the package_name (if specified) or project_name.
        # Links:
        # - https://labdmitriy.github.io/blog/distributions-vs-packages/
        # - Normalized package names: https://packaging.python.org/en/latest/specifications/name-normalization/ and `packaging.utils`
        self.project_name = project_name
        self.package_name = package_name or re.sub(
            r"[^a-zA-Z0-9_]+", "_", distribution_name or project_name.lower()
        )
        self.distribution_name = distribution_name or re.sub(
            r"[^a-zA-Z0-9\-]+", "-", self.package_name
        )
        self.project_path = parent_dir / project_name
        self.package_path = parent_dir / self.project_name / self.package_name
        self.version = version
        self._pre_validate()

    @property
    def wheel_name(
        self,
        build_tag: Optional[str] = None,
        python_tag: str = "py3",
        abi_tag: str = "none",
        platform_tag: str = "any",
    ) -> str:
        """
        build_tag: Optional build number. Must start with a digit.
        python_tag: E.g. ‘py27’, ‘py2’, ‘py3’.
        abi_tag: E.g. ‘cp33m’, ‘abi3’, ‘none’.
        platform_tag: E.g. ‘linux_x86_64’, ‘any’.
        """
        # https://peps.python.org/pep-0491/#file-name-convention
        escaped_distribution_name = re.sub(
            r"[^\w\d.]+", "_", self.distribution_name, re.UNICODE
        )
        if build_tag is not None:
            assert build_tag[0].isdigit(), "Build tag must start with a digit"
            build_tag += f"-{build_tag}"

        return f"{escaped_distribution_name}-{self.version}{build_tag}-{python_tag}-{abi_tag}-{platform_tag}.whl"

    def _pre_validate(self):
        if not self.package_name.isidentifier():
            raise ValueError(
                f"Invalid package name: {self.package_name}. Package names must be valid Python identifiers."
            )
        if not re.match(r"^[a-zA-Z0-9\-_]+$", self.distribution_name):
            raise ValueError(
                f"Invalid distribution name: {self.package_name}. Distribution names may only contain letters, numbers and hyphens."
            )
