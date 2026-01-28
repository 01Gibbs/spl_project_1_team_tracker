#!/usr/bin/env python3
"""
Boundary enforcement tool for hexagonal architecture.
Detects architectural violations as they emerge naturally.
"""

import ast
import sys
from pathlib import Path
from typing import List, Tuple


class BoundaryViolation:
    def __init__(self, file_path: Path, line: int, message: str):
        self.file_path = file_path
        self.line = line
        self.message = message

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line} - {self.message}"


class BoundaryChecker(ast.NodeVisitor):
    """Detects architectural boundary violations in Python code."""

    def __init__(self, file_path: Path, project_root: Path):
        self.file_path = file_path
        self.project_root = project_root
        self.violations: List[BoundaryViolation] = []

    def visit_ImportFrom(self, node):
        """Check import statements for boundary violations."""
        if node.module is None:
            return

        # Domain layer violations
        if self.is_domain_layer():
            if self.is_framework_import(node.module):
                self.violations.append(
                    BoundaryViolation(
                        self.file_path,
                        node.lineno,
                        f"Domain layer importing framework: {node.module}"
                    )
                )

        # Application layer violations
        if self.is_application_layer():
            if self.is_infrastructure_import(node.module):
                self.violations.append(
                    BoundaryViolation(
                        self.file_path,
                        node.lineno,
                        f"Application layer importing infrastructure: {node.module}"
                    )
                )

        self.generic_visit(node)

    def is_domain_layer(self) -> bool:
        """Check if file is in domain layer."""
        return "domain" in self.file_path.parts

    def is_application_layer(self) -> bool:
        """Check if file is in application layer."""
        return "application" in self.file_path.parts

    def is_framework_import(self, module: str) -> bool:
        """Check if import is a framework (forbidden in domain)."""
        frameworks = ['fastapi', 'sqlalchemy', 'requests', 'pydantic']
        return any(module.startswith(fw) for fw in frameworks)

    def is_infrastructure_import(self, module: str) -> bool:
        """Check if import is infrastructure (forbidden in application)."""
        infrastructure = ['sqlalchemy', 'requests', 'redis', 'boto3']
        return any(module.startswith(infra) for infra in infrastructure)


def check_file(file_path: Path, project_root: Path) -> List[BoundaryViolation]:
    """Check a single Python file for boundary violations."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content, filename=str(file_path))
        checker = BoundaryChecker(file_path, project_root)
        checker.visit(tree)
        
        return checker.violations
    
    except SyntaxError as e:
        return [BoundaryViolation(file_path, e.lineno or 0, f"Syntax error: {e.msg}")]
    except Exception as e:
        return [BoundaryViolation(file_path, 0, f"Error checking file: {e}")]


def main():
    """Check all Python files for boundary violations."""
    if len(sys.argv) > 1:
        project_root = Path(sys.argv[1])
    else:
        project_root = Path.cwd()

    # Find all Python files in src/
    src_path = project_root / "backend" / "src"
    if not src_path.exists():
        print(f"❌ No src directory found at {src_path}")
        sys.exit(1)

    python_files = list(src_path.rglob("*.py"))
    
    if not python_files:
        print("✅ No Python files found to check")
        return

    all_violations = []
    
    for file_path in python_files:
        violations = check_file(file_path, project_root)
        all_violations.extend(violations)

    if all_violations:
        print("❌ Boundary violations detected:")
        for violation in all_violations:
            print(f"  {violation}")
        sys.exit(1)
    else:
        print("✅ No boundary violations found")


if __name__ == "__main__":
    main()