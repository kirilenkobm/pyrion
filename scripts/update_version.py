#!/usr/bin/env python3
"""
Version management script for pyrion.

Updates version across all files that reference it:
- pyrion/_version.py (single source of truth)
- README.md (version badge)
- Regenerates API documentation with new version
"""

import re
import sys
from pathlib import Path
import argparse
import subprocess


def update_version_file(version: str) -> None:
    """Update the _version.py file."""
    version_file = Path("pyrion/_version.py")
    
    content = f'''"""Version information for pyrion."""

__version__ = "{version}"
__version_info__ = tuple(int(x) for x in __version__.split("."))

# Additional version metadata
__author__ = "Bogdan M. Kirilenko"
__github__ = "https://github.com/kirilenkobm"
__license__ = "MIT"
__copyright__ = "Copyright 2025 Bogdan M. Kirilenko"
'''
    
    version_file.write_text(content)
    print(f"✅ Updated {version_file} to version {version}")


def update_readme_badge(version: str) -> None:
    """Update the version badge in README.md."""
    readme_file = Path("README.md")
    
    if not readme_file.exists():
        print("❌ README.md not found")
        return
    
    content = readme_file.read_text()
    
    # Update version badge
    old_pattern = r'!\[version\]\(https://img\.shields\.io/badge/version-[^-]+-blue\)'
    new_badge = f'![version](https://img.shields.io/badge/version-{version}-blue)'
    
    updated_content = re.sub(old_pattern, new_badge, content)
    
    if content != updated_content:
        readme_file.write_text(updated_content)
        print(f"✅ Updated README.md badge to version {version}")
    else:
        print(f"ℹ️  README.md badge already at version {version}")


def regenerate_api_docs() -> None:
    """Regenerate API documentation with new version."""
    try:
        result = subprocess.run([sys.executable, "scripts/generate_api_docs.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Regenerated API documentation")
            if result.stdout:
                print(f"   {result.stdout.strip()}")
        else:
            print(f"❌ Failed to regenerate API docs: {result.stderr}")
    except Exception as e:
        print(f"❌ Error regenerating API docs: {e}")


def validate_version(version: str) -> bool:
    """Validate version format (semantic versioning)."""
    pattern = r'^\d+\.\d+\.\d+(?:\.(?:dev|alpha|beta|rc)\d*)?$'
    return bool(re.match(pattern, version))


def get_current_version() -> str:
    """Get current version from _version.py."""
    version_file = Path("pyrion/_version.py")
    
    if not version_file.exists():
        return "unknown"
    
    content = version_file.read_text()
    match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
    
    if match:
        return match.group(1)
    
    return "unknown"


def bump_version(current: str, part: str) -> str:
    """Bump version part (major, minor, patch)."""
    if current == "unknown":
        return "0.0.1"
    
    try:
        major, minor, patch = map(int, current.split('.'))
        
        if part == 'major':
            return f"{major + 1}.0.0"
        elif part == 'minor':
            return f"{major}.{minor + 1}.0"
        elif part == 'patch':
            return f"{major}.{minor}.{patch + 1}"
        else:
            raise ValueError(f"Invalid version part: {part}")
    
    except ValueError as e:
        print(f"❌ Error parsing version '{current}': {e}")
        return current


def main():
    """Main version management function."""
    parser = argparse.ArgumentParser(description="Manage pyrion version")
    parser.add_argument("--set", metavar="VERSION", help="Set specific version (e.g., 1.2.3)")
    parser.add_argument("--bump", choices=['major', 'minor', 'patch'], 
                       help="Bump version part")
    parser.add_argument("--show", action='store_true', help="Show current version")
    parser.add_argument("--docs-only", action='store_true', 
                       help="Only regenerate documentation")
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    import os
    os.chdir(project_root)
    
    current_version = get_current_version()
    
    if args.show:
        print(f"Current version: {current_version}")
        return
    
    if args.docs_only:
        regenerate_api_docs()
        return
    
    new_version = None
    
    if args.set:
        if not validate_version(args.set):
            print(f"❌ Invalid version format: {args.set}")
            print("Use semantic versioning: major.minor.patch[.dev|alpha|beta|rc]")
            sys.exit(1)
        new_version = args.set
    
    elif args.bump:
        new_version = bump_version(current_version, args.bump)
    
    else:
        print("❌ Must specify --set VERSION, --bump PART, --show, or --docs-only")
        parser.print_help()
        sys.exit(1)
    
    if new_version and new_version != current_version:
        print(f"🔄 Updating version from {current_version} to {new_version}")
        
        # Update all version references
        update_version_file(new_version)
        update_readme_badge(new_version)
        regenerate_api_docs()
        
        print(f"🎉 Version update complete: {new_version}")
        print("\nNext steps:")
        print("1. Test the package: python -c 'import pyrion; print(pyrion.__version__)'")
        print("2. Commit changes: git add -A && git commit -mm39.chrM.2bit 'Bump version to {}'".format(new_version))
        print("3. Tag release: git tag v{}".format(new_version))
        print("4. Build package: python -mm39.chrM.2bit build")
        print("5. Upload to PyPI: python -mm39.chrM.2bit twine upload dist/*")


if __name__ == "__main__":
    main() 