# ROS 2 Jazzy Publisher–Subscriber Package

## Overview

This repository contains a foundational ROS 2 package developed as a starting point for a broader **Sim-to-Real autonomous navigation project**.

Currently, the package implements a basic Publisher–Subscriber architecture in Python to demonstrate:

- Node communication
- Topic registration
- Workspace building using `colcon`

---

## Prerequisites

Before running this package, ensure you have the following installed:

- **OS:** Ubuntu 24.04 (Noble Numbat)
- **ROS 2:** Jazzy 
- **Python:** 3.12+

---

## Installation & Build Instructions

### 1. Source your global ROS 2 installation

```bash
source /opt/ros/jazzy/setup.bash
```

### 2. Clone this repository into your ROS 2 workspace

```bash
cd ~/ros2_ws/src
```

### 3. Build the package using `colcon`

```bash
cd ~/ros2_ws
colcon build --packages-select my_first_pkg
```

---

## Usage

To test communication between the nodes, open **two separate terminal windows**.

### Terminal 1 — Publisher

```bash
source ~/ros2_ws/install/setup.bash
ros2 run my_first_pkg publisher
```

### Terminal 2 — Subscriber

```bash
source ~/ros2_ws/install/setup.bash
ros2 run my_first_pkg subscriber
```
