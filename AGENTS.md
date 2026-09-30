# AGENTS.md

## Browser testing behind the GCB login

Auth-gated `*.gcb.io` apps sign in through the GCB IdP (id.gcb.io). For checking pages in a browser there is a test account with persistent access: `jelmer+2@gcb.io`. Its password lives on lux in `~/.config/gcb/brand-test-account.env` (`GCB_TEST_EMAIL`, `GCB_TEST_PASSWORD`, mode 600). Read it from there at runtime; never copy it into code, commits, logs, or chat.

- Sign in with this account instead of working around the login. Do not add auth bypasses (secret headers, `customCheck` hooks, extra `openPaths`) to `proxy.ts` or `gcb.toml` for testing.
- When a human has to see or finish the login, use a visible browser on lux (`DISPLAY=:0`), not a headless one.
