# Prism - PR Title Validator

Prism is a GitHub Action that validates pull request titles to ensure they follow conventional commit standards.

## Usage

```yaml
uses: MukhteshPendem/prism@main
with:
  github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Conventional Commit Rules

- `feat`: A new feature
- `fix`: A bug fix
- `chore`: Routine tasks like config updates
- `docs`: Documentation-only changes
- `test`: Adding or updating tests
- `refactor`: Code changes that neither fix a bug nor add a feature
- `style`: Code style improvements (formatting, whitespace)
- `perf`: Performance improvements
- `ci`: CI/CD configuration changes

## Example Commit Messages

- `feat: add PR title validation`
- `fix: resolve API token issue`
- `chore: add Docker support`
- `docs: update README`
- `test: add unit tests for PR validation`
- `refactor: simplify validation logic`
- `style: format code`
- `perf: optimize API call performance`
- `ci: add GitHub Actions workflow`
