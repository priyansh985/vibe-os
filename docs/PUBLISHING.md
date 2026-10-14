# Repository publication and release checklist

## Publish this project

1. Sign in to the GitHub account that should own the project.
2. Create a repository named **vibe-os**, ideally with default branch **main**.
3. If using the GitHub connector to upload after creating the repo, initialize with a README so the default branch exists; replace that starter README with the provided project README during import. If pushing locally using the prepared Git bundle, create an **empty** remote instead.
4. Import all tracked project files, including hidden `.github/` paths and `.gitignore`.
5. Verify the README, MIT license, skill file and installation guide render correctly.
6. Check **Actions** for a CI run and inspect the test matrix and build job. Do not claim CI passed until results are visible.
7. Optionally configure issue templates, public/private visibility, branch protection and private vulnerability reporting in GitHub settings.
8. To release v1.0.0, create a `v1.0.0` Git tag/release only after confirming the published source matches this build and tests are green.

## Push from the prepared Git bundle

If a Git bundle has been provided with this release, you can run:

```bash
git clone --branch main VIBE-OS-v1.0.0.bundle vibe-os
cd vibe-os
git remote remove origin
git remote add origin https://github.com/priyansh985/vibe-os.git
git push -u origin main
```

The bundle contains a local Git commit, but cannot create the remote repository. Authentication and repository ownership are managed by GitHub. If the remote was initialized with a README, do **not** use the commands above without first reconciling its history; import files via the connector or a normal clone instead.

## Release cautions

VIBE-OS v1 is not proven to improve productivity and does not securely sandbox agent-executed checks. Do not enable arbitrary verification commands from unknown pull requests or depend on the package as a security boundary. This repository's CI tests run project-authored code from incoming pull requests with read-only token permissions.

## Publish Node installer to npm (optional, separate action)

The repository contains a Node.js `package.json` and `bin/vibe-os.cjs` so it can already be installed with `npx github:priyansh985/vibe-os` or `npm install -g github:priyansh985/vibe-os`. Those commands do not require an npm registry publication.

Only a maintainer authenticated to an npm account that owns the name should publish:

```sh
npm test
npm pack --dry-run
npm view vibe-os name version   # verify name ownership/availability
npm login
npm publish --access public
```

If `vibe-os` is unavailable, choose an npm scope you control and update `package.json` + examples before publishing. **Do not claim bare `npx vibe-os` works until a published package is verified.** See [Node installation](NODE_INSTALLATION.md).
