# AGENTS.md

## Browsing apps behind the GCB login

Auth-gated `*.gcb.io` apps sign in through the GCB IdP (id.gcb.io). Agents never sign in as a person: they act as the host's machine identity, owned by the user who approved it and limited to the capabilities it was given (id.gcb.io `docs/machines.md`).

- `gcb machine status` shows the machine on this host. If there is none, run `gcb machine enroll <agent>-<host> --scopes <app>:member` and ask the user to approve the printed admin.gcb.io link.
- `gcb machine browse <app> /path` prints a one-time URL (60 s, single use) that opens the app as the machine; `gcb machine curl <app> /path` calls it without a browser.
- Tokens and one-time URLs are credentials: never paste them into chat, files or commits. Never use a person's account or copy their cookies.
- Do not add auth bypasses (secret headers, `customCheck` hooks, extra `openPaths`) to `proxy.ts` or `gcb.toml` for testing.
