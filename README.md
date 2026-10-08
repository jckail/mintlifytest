# Mintlify documentation starter

A public [Mintlify](https://mintlify.com) starter used to explore MDX documentation. This repository contains the site configuration, four documentation pages and Mintlify’s original logo/favicon assets. It does not implement an application backend or an API reference.

**Status:** docs-tooling experiment. The content is the upstream starter plus two maintenance guides; no hosted deployment has been verified.

## Documentation

- [Introduction](index.mdx) and [Quickstart](quickstart.mdx) — the starter's site pages.
- [Architecture](docs/architecture.mdx) — how configuration, pages and assets fit together.
- [Developer guide](docs/developer-guide.mdx) — maintaining and checking the site.
- [docs.json](docs.json) — site configuration and navigation; [AGENTS.md](AGENTS.md) — instructions for coding agents (still the upstream template).

## Preview and check

Use Node.js 22 and run these commands from the repository root:

```bash
npx --yes mint@4.2.970 dev
```

The CLI is pinned to the version checked for this audit. It downloads dependencies on first use and serves the local preview at `http://localhost:3000`.

```bash
python3 scripts/check-docs.py
npx --yes mint@4.2.970 broken-links
npx --yes mint@4.2.970 validate
```

The Python check uses the standard library to verify local navigation, content links, assets and basic source structure. It is not an MDX compiler. GitHub Actions also runs the pinned Mintlify link/build validation commands. Read the actual CI result before claiming the rendered site is verified.

## Customize and publish

Edit MDX content and add new page paths to `docs.json`. Keep Mintlify components and root-relative extensionless links in site pages. The repository retains the `mint` theme, green palette and upstream navigation/resource links.

Publishing requires a Mintlify project connected to this repository through the dashboard. A repository connection, deployment URL and hosted publication have not been verified here; pushing a commit alone does not establish that setup.

## License

The starter and original assets are from Mintlify. Preserve the [MIT license](LICENSE), including its copyright notice, when adapting them. See the official [CLI reference](https://www.mintlify.com/docs/cli/commands), [navigation guide](https://www.mintlify.com/docs/organize/navigation) and [component documentation](https://www.mintlify.com/docs/components).
