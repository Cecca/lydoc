#!/bin/bash

VERSION_FILE=lydoc/_version.py

## First of all, check if there are uncommitted changes. If so, abort.

if [[ $(git diff --shortstat 2> /dev/null | tail -n1) != "" ]]
then
    echo "There are uncommitted changes, commit them!"
    exit 1
fi

NEW_VERSION=$1
if [[ -z "$NEW_VERSION" ]]
then
    OLD_VERSION=$(python setup.py --version)
    echo "The old version is $OLD_VERSION"
    read -p "Enter the new version: " NEW_VERSION
fi

read -p "New version is $NEW_VERSION, continue? (y/n) " CONTINUE
case $CONTINUE in
    y)
        echo "Continuing with version $NEW_VERSION"
        ;;
    *)
        echo "Aborting"
        exit 1
        ;;
esac

echo "Write new version to $VERSION_FILE"
cat <<EOF >$VERSION_FILE
__version__ = "$NEW_VERSION"
EOF

echo "Committing changes"
git add $VERSION_FILE
git commit -m "Bump version to $NEW_VERSION"

echo "Tagging the release"
git tag -a $NEW_VERSION

echo "Bump to development version"
NEW_VERSION_LIST=(`echo $NEW_VERSION | tr "." " "`)
NEW_VERSION_LIST[2]=$(( ${NEW_VERSION_LIST[2]} + 1 ))
NEW_VERSION=$(echo ${NEW_VERSION_LIST[@]} | tr " " ".")
NEW_VERSION="$NEW_VERSION.dev1"

echo "Bumping to $NEW_VERSION"

echo "Write new version to $VERSION_FILE"
cat <<EOF >$VERSION_FILE
__version__ = "$NEW_VERSION"
EOF

echo "Committing changes"
git add $VERSION_FILE
git commit -m "Bump version to $NEW_VERSION"
