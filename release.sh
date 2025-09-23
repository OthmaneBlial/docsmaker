#!/bin/bash

set -e

echo "🚀 Starting release process..."

# Ensure build tooling is available
if ! command -v twine &> /dev/null || ! python -c "import build" 2>/dev/null; then
    echo "📦 Installing build + twine tooling..."
    python -m pip install --upgrade --quiet build twine
fi

if ! command -v twine &> /dev/null; then
    echo "❌ Failed to install Twine; aborting."
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

# Clean previous build outputs to avoid re-upload conflicts
echo "🧹 Cleaning old build artifacts..."
rm -rf build dist *.egg-info
echo "✅ Removed old build artifacts"

# Build package
echo "🔨 Building package..."
python -m build
if [ $? -ne 0 ]; then
    echo "❌ Build failed. Aborting release."
    exit 1
fi
echo "✅ Package built successfully"

# Validate built distributions
echo "🔍 Running twine check..."
twine check dist/*
if [ $? -ne 0 ]; then
    echo "❌ Distribution validation failed."
    exit 1
fi
echo "✅ Distributions validated"

# Check PyPI authentication configuration
echo "🔐 Checking PyPI authentication..."
# Fail fast if placeholder tokens are still in use
placeholder="pypi-XXXXXXXXXXXXXXXXXXXXXXXX"
detect_placeholder() {
    local value="$1"
    if [[ "$value" == *"$placeholder"* ]]; then
        echo "❌ Placeholder PyPI token detected."
        echo "Please create a real API token from https://pypi.org/manage/account/token/ and update your credentials."
        echo "You can store it in ~/.pypirc or export TWINE_PASSWORD before running this script."
        exit 1
    fi
}

if [ -z "$TWINE_USERNAME" ] || [ -z "$TWINE_PASSWORD" ]; then
    config_file=""
    if [ -f ./.pypirc ]; then
        config_file="./.pypirc"
    elif [ -f ~/.pypirc ]; then
        config_file="$HOME/.pypirc"
    fi

    if [ -z "$config_file" ]; then
        echo "❌ PyPI authentication not configured."
        echo "Please set up authentication using one of the following methods:"
        echo ""
        echo "Method 1: Create ~/.pypirc or ./.pypirc file:"
        echo "Create a file at ~/.pypirc or ./.pypirc with the following content:"
        echo "[pypi]"
        echo "username = __token__"
        echo "password = pypi-XXXXXXXXXXXXXXXXXXXXXXXX"
        echo ""
        echo "Method 2: Set environment variables:"
        echo "export TWINE_USERNAME=__token__"
        echo "export TWINE_PASSWORD=pypi-XXXXXXXXXXXXXXXXXXXXXXXX"
        echo ""
        echo "For more information, see: https://twine.readthedocs.io/en/latest/#configuration"
        exit 1
    fi

    echo "✅ .pypirc file found. Using credentials from $config_file"
    if grep -q "$placeholder" "$config_file"; then
        detect_placeholder "$placeholder"
    fi
else
    detect_placeholder "$TWINE_PASSWORD"
    echo "✅ Twine credentials set via environment variables."
fi

# Choose repository (default PyPI)
read -p "Upload repository (pypi/testpypi) [pypi]: " repo_choice
repo_choice=${repo_choice:-pypi}

# Upload to selected repository
echo "📤 Uploading to $repo_choice..."
twine upload --repository "$repo_choice" dist/*
if [ $? -ne 0 ]; then
    echo "❌ Upload failed. Aborting release."
    exit 1
fi
echo "✅ Successfully uploaded to $repo_choice"

echo "🎉 Release $new_version complete!"
