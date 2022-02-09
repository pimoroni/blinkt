# Blinkt! Simulator

A Tk based server to simulate Blinkt! on your Windows, Linux or macOS PC.

Works by hijacking the `blinkt` library and replacing it with a FIFO pipe to the Tk based simulator.

## Usage

Set the `PYTHONPATH` variable to the simulator directory and run an example. The fake `blinkt` will be loaded instead of the real one and output will launch in a new window:

```
PYTHONPATH=simulator python3 examples/rainbow.py
```
