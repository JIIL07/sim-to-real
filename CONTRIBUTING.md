# Contributing to Sim-to-Real Mobile Navigation

Thank you for contributing! This repository hosts the full pipeline for autonomous navigation of a mobile platform (differential drive, 2× RPLIDAR, IMU): first in Gazebo simulation, then on real hardware with quantitative sim-to-real gap analysis.

**Stack:** ROS 2 Jazzy · Gazebo · Nav2 · SLAM Toolbox · `ira_laser_tools` / `laserscan_multi_merger`

---

## Table of contents

- [Getting started](#getting-started)
- [Development workflow](#development-workflow)
- [Issues](#issues)
- [Pull requests](#pull-requests)
- [CI/CD](#cicd)
- [Code style](#code-style)
- [Documentation](#documentation)
- [Simulation and sim-to-real](#simulation-and-sim-to-real)
- [Repository layout](#repository-layout)

---

## Getting started

1. Accept the GitHub collaborator invite.
2. Clone the repository and sync `main`:

   ```bash
   git clone https://github.com/JIIL07/sim-to-real.git
   cd sim-to-real
   git pull origin main
   ```

3. Set up ROS 2 Jazzy on **Ubuntu 24.04** (see below).
4. Confirm the workspace builds cleanly before starting work.

### Development environment

This repository **is** the ROS 2 workspace (packages live in `src/`).

```bash
# ROS 2 Jazzy — https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
sudo apt install ros-jazzy-desktop ros-dev-tools

source /opt/ros/jazzy/setup.bash

git clone https://github.com/JIIL07/sim-to-real.git
cd sim-to-real
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Install additional project dependencies (Gazebo, Nav2, SLAM Toolbox, laser merger packages, etc.) as packages are added — document new deps in the relevant package `README.md`.

---

## Development workflow

```
pull main → branch dev/<feat-name> → work → commit → push → open PR → review → merge
```

### 1. Sync with `main`

```bash
git checkout main
git pull origin main
```

### 2. Create a branch

Branch **from up-to-date `main`**. Naming:

```
dev/<short-task-description>
```

Examples:

| Task | Branch |
|------|--------|
| Platform URDF model | `dev/urdf-platform-model` |
| Gazebo corridor world | `dev/gazebo-corridor-world` |
| Dual lidar merging | `dev/dual-lidar-merge` |
| Nav2 local planner tuning | `dev/nav2-local-planner-tune` |
| Lidar extrinsics calibration | `dev/lidar-extrinsics-calib` |
| Sim-to-real metrics | `dev/sim2real-metrics` |

```bash
git checkout -b dev/<feat-name>
```

Branch rules:

- lowercase Latin letters, words separated by `-`;
- no spaces or special characters;
- one branch per logical task — do not mix unrelated changes.

### 3. Work on the task

- Keep commits small and focused.
- Rebase onto `main` if the branch lives for several days:

  ```bash
  git fetch origin
  git rebase origin/main
  ```

### 4. Commits

[Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <short description>

[optional body — what and why]
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `sim`, `hardware`

**Scopes (examples):** `urdf`, `gazebo`, `lidar`, `slam`, `nav2`, `calib`, `sim2real`, `metrics`

Examples:

```
feat(urdf): add differential drive platform with dual RPLIDAR mounts
fix(lidar): correct frame_id for rear laser scan merger
sim(gazebo): add corridor test world with static obstacles
docs(nav2): document local planner parameter tuning rationale
hardware(calib): add IMU noise model from real sensor logs
```

### 5. Push and open a PR

```bash
git push -u origin dev/<feat-name>
```

Open a PR targeting `main` on GitHub (see [Pull requests](#pull-requests)).

**Do not push directly to `main`** — all changes go through PR and review.

---

## Issues

Before non-trivial work, **open an Issue** or pick an existing one. This avoids duplicate effort and records context for sim-to-real experiments.

### When to open an Issue

- new functionality (model, world, package, pipeline);
- bug in simulation or on real hardware;
- calibration / sim-to-real gap work;
- research (SLAM choice, planner comparison);
- infrastructure (CI, documentation).

### Issue template

```markdown
## Description
Brief: what needs to be done and why.

## Context
- Simulation / hardware / both
- Related packages: `...`
- Related issues: #...

## Acceptance criteria
- [ ] ...
- [ ] ...

## Additional info
Screenshots, logs, parameter links, expected metrics.
```

### Suggested labels

| Label | Purpose |
|-------|---------|
| `sim` | Gazebo, URDF/SDF, sensor plugins |
| `hardware` | Real platform, drivers, ROS ↔ hardware |
| `sim2real` | Calibration, gap analysis, parameter transfer |
| `slam` | SLAM Toolbox / mapping |
| `nav2` | Planning, BT, recovery |
| `lidar` | RPLIDAR, merger, extrinsics |
| `calibration` | IMU, odometry, lidars |
| `metrics` | Success rate, time-to-goal, path length |
| `bug` | Defect |
| `docs` | Documentation |
| `good first issue` | Starter task |

### Linking Issues and PRs

In the PR description use `Closes #<number>` or `Related to #<number>`.

---

## Pull requests

### Pre-merge checklist

- [ ] Branch is based on current `main`, named `dev/<feat-name>`
- [ ] `colcon build --symlink-install` succeeds
- [ ] Change tested in Gazebo **or** explicitly marked hardware-only / docs-only
- [ ] New parameters and launch files are documented
- [ ] No build artifacts committed (`build/`, `install/`, `log/`, binary logs)
- [ ] Issue created or referenced
- [ ] GitHub Actions CI passes (`Build and test`)

### PR description template

```markdown
## Summary
What was done and why (1–3 sentences).

## Changes
- ...

## Testing
How it was verified:
- [ ] `colcon build --symlink-install`
- [ ] Gazebo: world `...`, scenario `...`
- [ ] Nav2: goal → success / recovery
- [ ] Hardware (if applicable): ...

## Sim-to-real impact
Does not affect / requires hardware calibration / metrics attached

## Screenshots / logs
RViz, Gazebo, metric plots when possible.

## Related issues
Closes #...
```

### Review

- At least **1 approval** before merge (urgent hotfixes — team agreement).
- Address review comments or reply in the thread.
- Delete the branch on GitHub after merge.

---

## CI/CD

Every push to `main` and every pull request runs the [**CI** workflow](.github/workflows/ci.yml) on Ubuntu 24.04 with ROS 2 Jazzy:

1. `rosdep install` — resolve package dependencies
2. `colcon build --symlink-install` — build the workspace
3. `colcon test` — run package tests (lint: flake8, pep257, etc.)

Run the same checks locally before opening a PR:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
colcon test
colcon test-result --verbose
```

### Branch protection (`main`)

Direct pushes to `main` are **not allowed**. All changes go through a PR with:

- at least **1 approving review**;
- passing CI status check **Build and test**.

Repository admins: enable protection once after the CI workflow has run on `main` at least once.

1. Repository → **Settings** → **Branches** → **Add branch ruleset** (or *Add classic branch protection rule*).
2. Target branch: `main`.
3. Enable **Require a pull request before merging** (1 approval).
4. Enable **Require status checks to pass** → select **Build and test**.
5. Enable **Require conversation resolution before merging** (recommended).
6. Save.

---

## Code style

### General

- Minimal diff: only what the task requires.
- Reuse existing launch files and parameters instead of duplicating.
- Put sim-to-real-sensitive parameters in YAML with comments explaining physical meaning.
- Magic numbers in code need a comment or belong in config.

### ROS 2 packages

- Standard `ament` layout (`package.xml`, `CMakeLists.txt` / `setup.py`).
- Package names: `snake_case`, domain-specific (`platform_description`, `gazebo_worlds`, `navigation_bringup`).
- Launch files: prefer Python (`*.launch.py`) over XML for new packages.
- TF: explicit `frame_id`, consistent tree `base_link` → sensors; document extrinsics.

### C++

- Standard: **C++17** (ROS 2 Jazzy).
- Style: [ROS 2 C++ Style Guide](https://docs.ros.org/en/jazzy/The-ROS2-Project/Contributing/Code-Style-Language-Versions.html) — `snake_case` for functions/variables, `PascalCase` for classes.
- Headers: `#pragma once` or include guards.
- Prefer `const` and references; avoid raw `new`/`delete`.
- Formatting: `clang-format` (use `.clang-format` from repo root when added).

### Python

- PEP 8, 4-space indent.
- Type hints on public functions in nodes and utilities.
- `ruff` / `flake8` — when CI is set up, code must pass.

### URDF / SDF / Gazebo

- Units: SI (meters, radians, kg).
- Link and joint names: clear and aligned with TF (`lidar_front_link`, `wheel_left_link`).
- Wheel physics: document friction, damping, max effort — critical for sim-to-real.
- Lidar and IMU plugins: noise models should match datasheets or calibration logs.

### YAML configs (Nav2, SLAM, merger)

- Comment non-obvious parameters (units, range, behavioral effect).
- Separate `sim` and `real` files when parameters diverge; shared values in `common/`.
- Do not commit machine-specific hardware paths; use launch arguments or env vars.

### ROS domain

- Default `ROS_DOMAIN_ID=0` — do not change without an Issue and team agreement.
- `RMW_IMPLEMENTATION` — same rule; affects everyone on the network.

---

## Documentation

Every non-trivial change includes documentation in the same PR.

### What to document

| Change | Where |
|--------|-------|
| New ROS package | `package_name/README.md` |
| URDF / platform model | `README` + TF diagram / sensor layout |
| Gazebo world | world description, spawn pose, test purpose |
| Launch file | arguments, run example, expected topics |
| Nav2 / SLAM params | key parameter table and tuning rationale |
| Calibration | procedure, data, results (extrinsics, IMU noise) |
| Sim-to-real experiment | scenario, metrics, conclusions, sim vs real diff |

### Minimum package README

```markdown
# package_name

## Purpose
...

## Dependencies
...

## Usage
...

## Topics / TF / services
...

## Parameters
...

## Sim / Real
Config differences and known limitations.
```

All documentation is written in **English** (same as code, commits, and branch names).

---

## Simulation and sim-to-real

The project targets **quantitative** comparison between simulation and reality. Keep this in mind when making changes.

### Project areas

1. **Platform model** — URDF/SDF: differential drive, wheel physics, 2× RPLIDAR, IMU with realistic noise.
2. **Gazebo worlds** — empty room, corridor, cluttered indoor space, dynamic scene (simple lab).
3. **Lidar fusion** — `ira_laser_tools` / `laserscan_multi_merger`, extrinsics calibration, 360° coverage.
4. **SLAM** — SLAM Toolbox (alternatives — discuss in an Issue).
5. **Navigation** — Nav2: global/local planner, behavior tree, recovery behaviors.
6. **Sim-to-real** — odometry, lidar, IMU, latency; calibration; re-validation on hardware.
7. **Metrics** — success rate, time-to-goal, path length, collisions on identical scenarios.

### Rules for sim-to-real PRs

- State which worlds/scenarios were used for verification.
- If physics or noise parameters change, include justification (datasheet, calibration, log reference).
- Avoid breaking sim/real config parity without documenting the change.

### Metrics (experimental PRs)

Minimum set for navigation scenarios:

| Metric | Description |
|--------|-------------|
| Success rate | % of goals reached |
| Time-to-goal | Start to goal duration |
| Path length | Trajectory length |
| Collisions | Contact / collision count |

Report as a sim vs real table plus a short conclusion in the PR or under `docs/experiments/`.

---

## Repository layout

```
.
├── README.md
├── CONTRIBUTING.md
├── .gitignore
├── .github/workflows/ci.yml
└── src/                    # ROS 2 packages
    └── ...
```

The repository root is the colcon workspace. Build artifacts (`build/`, `install/`, `log/`) are not committed (see `.gitignore`).

---

## Questions

Not sure where to start? Open an Issue with the `question` label or comment on an existing one. Small doc fixes can skip an Issue, but still use a `dev/<feat-name>` branch.
