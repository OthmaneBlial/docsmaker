#!/bin/bash

set -e

echo "🚀 Starting release process..."

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "❌ Twine not installed. Install with: pip install twine"
    exit 1
fi

# Get current version
current_version=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
echo "📦 Current version: $current_version"

# Prompt for version bump type
read -p "Enter version bump type (patch/minor/major): " bump_type

# Parse current version (assuming semver format)
IFS='.' read -r major minor patch <<< "$current_version"

case $bump_type in
    patch)
        patch=$((patch + 1))
        ;;
    minor)
        minor=$((minor + 1))
        patch=0
        ;;
    major)
        major=$((major + 1))
        minor=0
        patch=0
        ;;
    *)
        echo "❌ Invalid bump type. Must be patch, minor, or major."
        exit 1
        ;;
esac

new_version="$major.$minor.$patch"
echo "📈 New version: $new_version"

# Confirm version bump
read -p "Proceed with version bump to $new_version? (y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "❌ Release cancelled."
    exit 0
fi

# Update version in pyproject.toml
sed -i "s/^version = .*/version = \"$new_version\"/" pyproject.toml
echo "✅ Updated version in pyproject.toml"

# Run tests
echo "🧪 Running tests..."
python -m pytest --color=yes -v --tb=short
if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Aborting release."
    exit 1
fi
echo "✅ Tests passed"

# Build package
echo "🔨 Building package..."
python -m build
if [ $? -ne 0 ]; then
    echo "❌ Build failed. Aborting release."
    exit 1
fi
echo "✅ Package built successfully"

# Check PyPI authentication configuration
echo "🔐 Checking PyPI authentication..."
if [ -z "$TWINE_USERNAME" ] || [ -z "$TWINE_PASSWORD" ]; then
    if [ ! -f ~/.pypirc ] && [ ! -f ./.pypirc ]; then
        echo "❌ PyPI authentication not configured."
        echo "Please set up authentication using one of the following methods:"
        echo ""
        echo "Method 1: Create ~/.pypirc or ./.pypirc file:"
        echo "Create a file at ~/.pypirc or ./.pypirc with the following content:"
        echo "[pypi]"
        echo "username = OthmaneBlial"
        echo "password = <your_PyPI_password>"
        echo ""
        echo "Method 2: Set environment variables:"
        echo "export TWINE_USERNAME=OthmaneBlial"
        echo "export TWINE_PASSWORD=<your_PyPI_password>"
        echo ""
        echo "For more information, see: https://twine.readthedocs.io/en/latest/#configuration"
        exit 1
    else
        echo "✅ .pypirc file found. Using credentials from ~/.pypirc or ./.pypirc"
    fi
else
    echo "✅ Twine credentials set via environment variables."
fi

# Upload to PyPI
echo "📤 Uploading to PyPI..."
twine upload dist/*
if [ $? -ne 0 ]; then
    echo "❌ Upload failed. Aborting release."
    exit 1
fi
echo "✅ Successfully uploaded to PyPI"

echo "🎉 Release $new_version complete!"