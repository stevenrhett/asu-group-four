# Contributing Guidelines

Welcome to the ASU Group Four project! To maintain a clean, collaborative, and high-quality codebase, we follow industry-standard GitHub workflows. Please read and follow these guidelines carefully.

## Git Workflow

### Branching Strategy
- **Main Branch (`main`)**: This is the production-ready branch. It should always contain stable, tested code. Direct pushes to `main` are **prohibited**.
- **Development Branch (`dev`)**: This is the integration branch for ongoing work. All feature branches should be merged here first via pull requests (PRs).
- **Feature Branches**: Create branches off `dev` for new features, bug fixes, or experiments. Name them descriptively, e.g., `feature/add-user-auth` or `bugfix/fix-login-error`.

### Workflow Steps
1. **Start from `dev`**: Always begin by checking out and pulling the latest `dev` branch.
   ```
   git checkout dev
   git pull origin dev
   ```
2. **Create a Feature Branch**: Work on your changes in a dedicated branch.
   ```
   git checkout -b feature/your-feature-name
   ```
3. **Commit Regularly**: Make small, meaningful commits with clear messages (e.g., "Add user authentication logic").
4. **Push to `dev` First**: Push your feature branch and create a PR to merge into `dev`.
   - Never push directly to `main`.
   - Ensure your branch is up-to-date with `dev` before pushing.
5. **Pull Request to `dev`**: 
   - Request reviews from at least one team member.
   - Address feedback and ensure tests pass (if applicable).
   - Merge only after approval.
6. **Pull Request to `main`**: Once `dev` has stable changes, create a PR from `dev` to `main`.
   - This should happen periodically (e.g., after a sprint or milestone).
   - Require thorough testing and multiple approvals.
7. **Merge Strategy**: Use "Squash and merge" for feature branches to keep history clean. Use "Merge commit" for `dev` to `main` to preserve context.

### Key Rules
- **Never Push to `main` Directly**: All changes must go through PRs to `dev` first, then to `main`.
- **Keep Branches Short-Lived**: Delete feature branches after merging to avoid clutter.
- **Rebase Frequently**: Rebase your feature branch on `dev` to stay current and avoid merge conflicts.
- **Use Descriptive Commits**: Follow conventional commit format (e.g., `feat: add login page`, `fix: resolve API timeout`).
- **Test Before Merging**: Run tests locally and ensure CI/CD passes.
- **Communicate**: Use PR descriptions and comments for context. Tag reviewers appropriately.

### Best Practices
- **Code Reviews**: Mandatory for all PRs. Focus on code quality, security, and adherence to standards.
- **Issue Tracking**: Create GitHub issues for tasks, bugs, or features. Link PRs to issues.
- **Documentation**: Update README, docs, or comments as needed.
- **Security**: Avoid committing secrets. Use environment variables.
- **Continuous Integration**: We use GitHub Actions for automated testing. Ensure your code doesn't break builds.
- **Conflict Resolution**: If conflicts arise, communicate with the team and resolve them carefully.
- **Backup**: Regularly push your work to avoid data loss.

By following these practices, we ensure a smooth, scalable development process. If you're new, ask for help—collaboration is key! Questions? Reach out in the team chat or via GitHub issues.
