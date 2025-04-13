# 🌌 Astrodynamics – Solved Exercises (UNSAM 2025)

This repository contains solved exercises from the **Astrodynamics** course at UNSAM (Universidad Nacional de San Martín), based on the 2025 syllabus.

The goal is to document and simulate orbital mechanics problems using Python — in particular, those from the official problem sets (e.g., **Guide No. 2**) used during the course.

## 📘 What’s included

- 📐 Orbital parameter computations (a, e, ε, h, p, etc.)
- 🔁 Conversions between orbital representations
- 📈 Plotting of conic sections (polar and Cartesian)
- ⚠️ Elliptic, hyperbolic, and parabolic orbit cases
- 🔬 Vallado’s algorithms (implemented in Python)
- 📎 Tools for true/mean/eccentric anomaly conversions
- 💻 Code compatible with `conda` virtual environments (e.g., `astroenv`)

---

## 📝 Guide 2 – Topics covered

The repository will progressively include all problems from **Astrodynamics Guide No. 2**, such as:

- Vallado Algorithms 2 to 6, 9, and 10 (implemented and validated)
- Figures 2-6 to 2-9 from Vallado (recreated for multiple eccentricities)
- Anomaly conversions (true ↔ mean ↔ eccentric)
- Time of flight computations
- Orbit propagation from initial conditions
- ECI vector evaluations at specific times
- TLE parsing and propagation using SGP4
- 3D plotting of orbits (Earth-centered)

Each solution includes clean code, comments, input/output descriptions, and at least one working usage example as required by the instructors.

---

## ⚙️ Requirements

- Python 3.10+
- numpy
- matplotlib
- sgp4 (for TLE propagation)

### Setup (using conda):

bash
conda create -n astroenv python=3.10 numpy matplotlib sgp4
conda activate astroenv

## ✍️ Author
Ezequiel Maceda
📍 Buenos Aires, Argentina
🛰️ System Engineer.

