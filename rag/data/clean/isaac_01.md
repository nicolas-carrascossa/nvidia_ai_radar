---
url: https://developer.nvidia.com/isaac
tecnologia: Isaac
titulo: Isaac - AI Robot Development Platform | NVIDIA Developer
---

1. [Home](https://developer.nvidia.com/)

Isaac

# NVIDIA Isaac

Ready to jump-start your AI robot development? NVIDIA Isaac™ is the ideal place to start. This open robotics development platform consists of [simulation](https://www.nvidia.com/en-us/use-cases/robotics-simulation/) and [robot learning](https://www.nvidia.com/en-us/use-cases/robot-learning/) frameworks, NVIDIA® CUDA®-accelerated libraries, AI models, and reference workflows to create autonomous mobile robots (AMRs), robot arms, manipulators, and [humanoids](https://www.nvidia.com/en-us/use-cases/humanoid-robots/).

* * *

## NVIDIA Isaac Libraries and AI Models

NVIDIA robotics full-stack CUDA-acceleration libraries and optimized AI models give you a better, more efficient way to develop, train, simulate, deploy, operate, and optimize robot systems.

## NVIDIA Isaac for Manipulation

### Motion Planning

NVIDIA cuMotion is an NVIDIA CUDA-accelerated library that helps solve robot motion planning problems at scale by running multiple trajectory optimizations simultaneously to return the best solution.

[Download the Library From GitHub](https://github.com/nvidia-isaac/cumotion/releases)

### Pose Estimation and Tracking

FoundationPose is a foundation model for 6D pose estimation and tracking of novel objects. It tracks and estimates the pose of unseen objects and can handle challenging object properties (textureless, glossy, tiny) and scenes with fast motion or severe occlusions.

[Download the Model From NGC](https://developer.nvidia.com/isaac)

### Depth Estimation

FoundationStereo is a foundation model designed to achieve strong zero-shot generalization for stereo matching.

[Download the Model From NGC](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tao/models/foundationstereo)

### Object Detection

SyntheticaDETR is a pretrained model for object detection in indoor environments. It can be used as a front end to pose estimators like FoundationPose, so it can localize objects using 2D bounding boxes before pose estimation.

[Download the Model From NGC](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/isaac/models/synthetica_detr)

### Isaac TeleOp

Collect high-quality human demonstrations through teleoperation in the real- world and simulation.

## NVIDIA Isaac for Mobility

### Real-Time 3D Occupancy Grid

Enable robots to identify obstacles in 3D spaces up to five meters away and generate a 2D costmap using the NVIDIA nvblox CUDA-accelerated 3D reconstruction library. Get results 100x faster than with CPU-centric methods.

### Accelerated Stereo Visual Odometry and SLAM

Accelerated Stereo Visual Odometry and SLAM

Get sub-1% trajectory errors for real-time, CUDA-accelerated visual SLAM across diverse sensors and platforms using NVIDIA cuVSLAM.

Seamlessly navigate environments with sparse visual features or repetitive patterns by fusing input from multiple viewpoints. Get started with [pycuVSLAM](https://github.com/NVlabs/PyCuVSLAM).

### Generalizable End-to-End Mobility

Train vision-based mobility foundation models using NVIDIA COMPASS, enabling navigation across robot types and changing environments.

The workflow includes [synthetic data generation](https://www.nvidia.com/en-us/glossary/synthetic-data-generation/) with NVIDIA Isaac Sim™ and Cosmos™ Transfer, model training and post-training in Isaac Lab, and deployment with [NVIDIA Jetson Orin™](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/) or [Thor](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/) ™.

#### NVIDIA Isaac ROS

NVIDIA Isaac ROS (Robot Operating System) is built on the open-source ROS 2. This collection of NVIDIA CUDA-accelerated computing packages and AI models streamlines and expedites the development of advanced AI robotics applications.

[Learn More About Isaac ROS](https://developer.nvidia.com/isaac/ros)

* * *

## Simulation and Robot Learning

Design, simulate, test, and train your AI-based robots and autonomous machines in a physically based virtual environment.

### NVIDIA Isaac Sim

NVIDIA Isaac Sim, built on [NVIDIA Omniverse](https://developer.nvidia.com/omniverse) ™, gives you a faster way to develop autonomous machines in a physically based virtual environment.

Together, [NVIDIA Cosmos](https://developer.nvidia.com/cosmos) ™ and Isaac Sim let you generate synthetic data from 3D scenes for training perception robots.

[Learn More About Isaac Sim](https://developer.nvidia.com/isaac/sim)

### NVIDIA Isaac Lab

This lightweight sample application is built on Isaac Sim and optimized for robot learning and robot foundation model training.

[Learn More About Isaac Lab](https://developer.nvidia.com/isaac/lab)

[Simplify Generalist Robot Policy Evaluation With Isaac Lab-Arena](https://developer.nvidia.com/blog/simplify-generalist-robot-policy-evaluation-in-simulation-with-nvidia-isaac-lab-arena/)

#### Newton, the Next-Generation Open-Source Physics Simulation Engine

Newton is an open-source, GPU-accelerated, and extensible physics engine, co-developed by Google DeepMind and Disney Research, and [managed by the Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-contribution-of-newton-by-disney-research-google-deepmind-and-nvidia-to-accelerate-open-robot-learning). Built on NVIDIA Warp and OpenUSD, Newton is optimized for robotics and compatible with learning frameworks such as MuJoCo Playground or Isaac Lab. [Newton Beta](https://github.com/newton-physics) is now available to use.

## NVIDIA Isaac GR00T for Humanoid Robot Development

NVIDIA Isaac GR00T is an open reference platform for general-purpose humanoid robots that enables developers to build, train, test, and deploy AI-powered robots.

It comprises open data and data pipelines, an open robot foundation model, simulation frameworks, middleware, NVIDIA CUDA-X™ accelerated runtime libraries, and NVIDIA Jetson Thor™ for real-time robot inference and control.

[Learn More About Isaac GR00T](https://developer.nvidia.com/isaac/gr00t)

* * *

## NVIDIA-Accelerated Systems

NVIDIA’s three computing platforms streamline and accelerate developer workflows: NVIDIA DGX™ systems for building robotics AI models, NVIDIA OVX™ for simulating, testing, and training them, and NVIDIA AGX™ for deploying and running them.

### NVIDIA DGX

The DGX platform combines the best of NVIDIA software and infrastructure—ideal for training multi-modal foundational models for robots.

[Learn More About NVIDIA DGX](https://www.nvidia.com/en-us/data-center/dgx-platform/)

### NVIDIA OVX

OVX systems provide industry-leading graphics and compute performance to accelerate the next generation of robotics.

[Learn More About NVIDIA OVX](https://www.nvidia.com/en-us/data-center/products/ovx/)

### NVIDIA AGX

AGX systems, including NVIDIA Jetson™, offer exceptional performance and energy efficiency, making them the leading platform for robotics. Trained, tested, and optimized robot AI models are deployed to these systems for real-world operation.

[Learn More About NVIDIA AGX](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/)

### NVIDIA OSMO

OSMO is a cloud-native workflow orchestration platform that lets you easily scale your workloads across distributed environments—from on-premises to private and public cloud resource clusters.

[Learn More About NVIDIA OSMO](http://developer.nvidia.com/osmo)

## Isaac Learning Resources

Tutorial

Isaac Lab \| Newton Physics Engine

### Train Quadruped Locomotion with Isaac Lab & Newton

Train quadruped locomotion policies and simulate cloth manipulation with Isaac Lab.

Explainer

Cosmos \| NVIDIA Isaac GROOT

### Cosmos World Foundation Models for Physical AI

Explore how Cosmos world foundation models accelerate physical AI development.

Tutorial

Isaac ROS \| Isaac Sim

### Beginner’s Guide: Robot Sim with ROS 2 & Isaac Sim

Build and test robot simulations using ROS 2 and Isaac Sim.

Explainer

NVIDIA Isaac GROOT

### Synthetic Motion Generation for Humanoid Robots

Explore synthetic motion generation pipelines for training humanoid robots.

Tutorial

Isaac Sim

### Train AMRs with Synthetic Data for Detection

Build an AMR perception model using synthetic data from Isaac Sim.

Overview

cuMotion \| Isaac ROS \| Isaac Sim

### Amazon Zero-Touch Manufacturing with Isaac & Digital Twins

See how Amazon uses Isaac Sim and digital twins for autonomous manufacturing.

**1 – 6** of 15

Show

6

[Download the raw results data (JSON)](https://developer.nvidia.com/search-data/robotics.json)

## Developer Resources and Support

### Explore the Community

### Get Training and Certification

### Join the Program for Startups

[Join the Program for Startups](https://www.nvidia.com/en-us/startups/ "Join the Program for Startups")

* * *

## Latest Robotics News

##### Loading...

Loading...

##### Loading...

Loading...

##### Loading...

Loading...

##### Loading...

Loading...