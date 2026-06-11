# Sim-to-Real Mobile Navigation

Autonomous navigation stack for a differential-drive mobile platform (2× RPLIDAR, IMU): develop and validate in **Gazebo**, then deploy on real hardware with quantitative **sim-to-real** analysis.

**Status:** early stage — workspace bootstrap and basic ROS 2 communication only.

**Stack:** ROS 2 Jazzy · Ubuntu 24.04 · Gazebo · Nav2 · SLAM Toolbox

---

## Current state

- ROS 2 Jazzy colcon workspace with a starter Python package (`my_first_pkg`)
- Publisher–subscriber demo to verify build and topic flow
- CI on pull requests (`colcon build` + lint tests)
- Contributing guidelines and branch workflow (`dev/<feat-name>` → PR)

---

## Roadmap

| Phase | Goal |
|-------|------|
| **1 — Platform model** | URDF/SDF: differential drive kinematics, wheel friction, dual RPLIDAR + IMU plugins with realistic noise |
| **2 — Simulation worlds** | Gazebo scenes: empty room, corridor, cluttered indoor, simple dynamic lab |
| **3 — Sensor fusion** | Merge two 2D lidars (`ira_laser_tools` / `laserscan_multi_merger`), extrinsics calibration for 360° coverage |
| **4 — SLAM** | SLAM Toolbox (or alternative) — mapping in sim and on hardware |
| **5 — Navigation** | Nav2: global/local planners, behavior tree, recovery behaviors, platform-specific tuning |
| **6 — Sim-to-real** | Measure gap (odometry, lidar, IMU, latency); calibrate models; re-validate on robot |
| **7 — Evaluation** | Same scenarios in sim vs real: success rate, time-to-goal, path length, collisions |

---

## Quick start

```bash
git clone https://github.com/JIIL07/sim-to-real.git
cd sim-to-real

source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

See [`src/README.md`](src/README.md) for running the demo nodes.

---

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) for branch workflow, code style, issues, and CI requirements.
