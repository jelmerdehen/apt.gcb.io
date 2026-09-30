# AGENTS.md

Shared rules: /data/p/gcb-agents/README.md

Static APT repository (Sileo/Zebra/apt) for rootless iOS packages (`iphoneos-arm64`, `/var/jb`),
currently `io.gcb.substrate-logger`. Not a gcb app: no `gcb.toml`, no build, no process.

## Release a package

1. Drop the `.deb` into `debs/` (keep older versions; clients may pin them).
2. `make generate` (runs `generate-repo.py`: needs `ar`; rewrites `Packages*` and `Release`).
3. Update `sileo-featured.json` / `index.html` if the featured package changed.
4. Commit and push, then publish (the webroot is a plain copy of the tracked files, owned by `j`):

```bash
rsync -av --exclude .git --exclude AGENTS.md --exclude CLAUDE.md -e 'ssh -p 31337' \
  ./ j@10.13.38.1:/var/www/apt.gcb.io/
```

## Serving

- saskia nginx `/etc/nginx/conf.d/apt.gcb.io.conf`, `root /var/www/apt.gcb.io`, `autoindex on`,
  CORS `*` and APT MIME types. Static files: nothing to restart.
- Check drift: compare `sha256sum` of `git ls-files` with the same files on saskia.
- Verify: `curl -sI https://apt.gcb.io/Release` and `.../debs/<file>.deb` (200,
  `application/vnd.debian.binary-package`).
- TLS cert `apt.gcb.io` is not in the `idgcb-certbot` renew list (see saskia.gcb.io AGENTS.md).
