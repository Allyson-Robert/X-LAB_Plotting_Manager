# Home
This project is a framework for integrating **data-processing and plotting** into a structured user-interface.
The aim of this project is two-fold
    1) Provide a straightforward way to collect and consistently plot data from a variety of sources.
    2) Provide a framework of modular data-processing and plotting components.

At a high level, it provides:

- Two user interface windows, one for creating **dataspecs** (which define what data to collect and how to process it) and one for launching and monitoring **analyses** (which execute dataspecs and plot the results)
- A set of **contracts / interfaces** that define how devices, processors, and plotters should behave
- A layer of general **utilities** for configuration and general plumbing
- An easy way to enable logging to the UIs console

Instead of hard-coding a single pipeline, the framework focuses on:

- **Modularity**
- **Component Reuse**
- **Ease of Extension**

## Documentation map

- [Getting started](getting_started.md)
- [Architecture](architecture.md)
- [Dataspecs](dataspecs.md)
- [Logging](logging.md)
