# Test AutoPub & GitHub Actions CI

1. Create repository
1. Create GitHub and PyPI tokens with appropriate scopes
1. Add `GH_TOKEN` & `PYPI_PASSWORD` environment variables via repository Settings > Secrets > New secret
1. Create `.github/workflows` and add appropriate GitHub CI workflow
1. Add appropriate AutoPub configuration to `pyproject.toml`
1. Add `RELEASE.md` file with release type and description
1. `git add .`, commit, and push
