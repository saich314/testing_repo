# Stacked PRs — the guide

## What is a stacked PR?

Instead of one giant PR with 1,500 changed lines, you split work into a
**chain of small PRs, each based on the previous one**:

```
main ← PR #1 (feat/subtract) ← PR #2 (feat/multiply) ← PR #3 (feat/divide)
```

Each PR's **diff only shows its own changes**, because its base branch is the
PR below it, not `main`. Reviewers see three 50-line PRs instead of one
150-line PR.

This repo is a live example:

```
* feat/divide     ← PR #3, base = feat/multiply
* feat/multiply   ← PR #2, base = feat/subtract
* feat/subtract   ← PR #1, base = main
* main
```

## Why bother?

- **Reviewable units.** A 50-line PR gets a real review in minutes; a
  1,500-line PR gets a rubber stamp ("LGTM") in a week.
- **You keep moving.** While PR #1 waits for review, you build PR #2 and #3
  on top of it instead of being blocked.
- **Independent merges.** PR #1 can merge as soon as it's approved, without
  waiting for the rest of the stack to be finished.
- **Better git history.** Each merged PR is one coherent, tested step.

## Building a stack

```bash
git checkout main
git checkout -b feat/subtract      # ...work, commit...
git checkout -b feat/multiply      # branched FROM feat/subtract — this is the stacking
                                   # ...work, commit...
git checkout -b feat/divide        # branched FROM feat/multiply
                                   # ...work, commit...
```

Then open PRs with each one's base set to the branch below it:

```bash
gh pr create --head feat/subtract --base main
gh pr create --head feat/multiply --base feat/subtract
gh pr create --head feat/divide   --base feat/multiply
```

## The hard part: keeping the stack in sync

Two events break a stack, and both are fixed by the same command, run from
the **top** branch (needs git ≥ 2.38):

**1. A review fix lands in a lower PR** (branches above are now stale):

```bash
git checkout feat/subtract         # ...apply the fix, commit...
git checkout feat/divide           # go to the TOP of the stack
git rebase feat/subtract --update-refs
```

**2. `main` moved** (someone else merged, or your bottom PR merged):

```bash
git checkout feat/divide           # TOP of the stack again
git rebase main --update-refs
```

`--update-refs` replays every commit in the chain **and moves each
intermediate branch label** (`feat/subtract`, `feat/multiply`) to its
replayed commit. Without it you'd have to rebase each branch one at a time
with `git rebase --onto`.

Make it the default so you never forget:

```bash
git config --global rebase.updateRefs true
```

After a restack, the branches were rewritten, so pushing requires force —
use the safe variant:

```bash
git push --force-with-lease origin feat/subtract feat/multiply feat/divide
```

## Merging the stack

Merge bottom-up:

1. Merge PR #1 (`feat/subtract` → `main`).
2. GitHub automatically retargets PR #2's base to `main`.
3. Restack the remainder (`git checkout feat/divide && git rebase main --update-refs`),
   force-push, and repeat.

Prefer **rebase-merge or fast-forward merges** for stacks. Squash-merging
works too, but after each squash the replayed commits look new to git, so
expect to resolve the same conflicts again when restacking (this is what
tools automate away).

## Tools that automate all of this

Hand-rolling works (you just did it), but at scale people use:

- **Graphite (`gt`)** — `gt create`, `gt restack`, `gt submit` manage the
  whole stack and its PRs for you.
- **git spr / spr** — turns each commit into its own PR.
- **ghstack** (Meta) — same idea, used with large monorepos.
- **jj (Jujutsu)** — a git-compatible VCS where restacking is automatic.

## Rules of thumb

- Keep each PR **one logical change** that passes tests on its own
  (every branch in this repo's stack has a green `python3 -m unittest`).
- Keep stacks short — 2–5 PRs. Ten deep becomes a rebase treadmill.
- Only stack when there's a real dependency; independent changes should be
  parallel branches off `main`, not a stack.
- Put the risky/controversial change at the **bottom** of the stack if you
  can — everything above it is hostage to its review.
