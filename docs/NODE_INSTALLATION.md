# Node.js / npm / npx installation

VIBE-OS includes a **native Node.js bootstrapper** for the portable coding-agent skill. It needs **Node.js 18+** and no Python runtime or third-party Node dependencies. The Node CLI installs the same skill files as the Python CLI, but it does **not** implement the Python CLI's `assess`, `task`, `verify`, `report`, or `score` commands.

## Use npx directly from GitHub — available before npm publication

Open a terminal in the **existing application project** you want to enhance, then run:

```sh
npx --yes github:priyansh985/vibe-os init --agent all
```

Alternative specifying the executable explicitly:

```sh
npx --yes --package=github:priyansh985/vibe-os vibe-os init --agent all
```

This downloads the Node package from this GitHub repository using npm and runs `vibe-os` in the current directory. The installer makes no network requests itself. `--yes` authorizes npm to download the package without its interactive confirmation.

To install only one adapter:

```sh
npx --yes github:priyansh985/vibe-os init --agent codex
npx --yes github:priyansh985/vibe-os init --agent claude
npx --yes github:priyansh985/vibe-os init --agent cursor
```

`--project path/to/app` changes the destination; omitting it uses the current directory. On success the project contains `.vibeos/` metadata plus the selected coding-agent skill/rule paths.

## npm install directly from GitHub

For a reusable global command:

```sh
npm install --global github:priyansh985/vibe-os
vibe-os init --project . --agent all
vibe-os doctor --project .
```

For a locally cloned copy of VIBE-OS:

```sh
npm install --global .
vibe-os --help
```

Because the package contains one `bin` executable, its GitHub-backed `npx` invocation can infer the `vibe-os` command.

## After publishing to npm registry

The short forms below **will work only after an authorized maintainer has published a package under the exact `vibe-os` name**, and only if that package name is available and owned by this project. Do not use an unrelated package with the same name.

```sh
npx vibe-os init --agent all
npm install --global vibe-os
vibe-os init --agent all
```

If the name `vibe-os` is unavailable, use a package you control, for example `@YOUR_NPM_USERNAME/vibe-os`, update `package.json` accordingly, and invoke `npx @YOUR_NPM_USERNAME/vibe-os init --agent all` instead.

Before publishing:

1. Run `npm test`, `npm pack --dry-run`, and inspect the packaged files.
2. Confirm ownership/availability of the npm package name via `npm view vibe-os` or the npm website.
3. Authenticate to npm (`npm login`) using your own credentials and 2FA.
4. Run `npm publish --access public` from the repository root (the npm publish action is **not** automated by this repository).
5. Verify the published package contents and `npx <published-name> --version` in a clean directory.

Publishing requires npm account access and is separate from pushing this repository to GitHub.

## Existing files and security

The installer preserves already-present files by default. Pass `--force` only if you want to overwrite **VIBE-OS-managed** files after reviewing any customizations. It does not delete extra files found in the existing skill directory. The installer refuses to traverse a project-relative symlink while writing.

The Node installer doesn't run project build scripts, invoke AI models, or execute tests. Running `npx` or `npm install` always entails npm downloading and executing the requested package; inspect the GitHub source and use a pinned commit or release for higher assurance.

## Using the full CLI

The full seven-command toolkit remains Python-based:

```sh
python -m pip install "git+https://github.com/priyansh985/vibe-os.git"
python -m vibeos --help
```

The Node installer and Python toolkit can both operate on the same project; both use `.vibeos/` state and the same bundled skill content.
