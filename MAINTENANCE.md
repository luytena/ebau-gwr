# Maintainer's Handbook

## Make a new release

We're using `python-semantic-release` to generate a changelog and suggest the next version.

1. Checkout `main` branch, ensure you have all tags
1. Figure out the next version
1. Update code (CHANGELOG, version info)
1. Pull Request with the version bump.
1. Create tag on the merge commit
1. Upload / edit change log


```
# Ensure you're on the current master and have all release tags
git checkout main
git pull origin --tags

# Prepare changelog
semantic-release changelog --noop --unreleased -D version_source=tag

# Figure out the next version
semantic-release version --noop -D version_source=tag
```
