# Logging

Logging provides insight into **what the framework is doing**, both internally and in your own extensions.  
It is especially important when:

- Running long or complex analyses
- Debugging failing devices, processors or plotters
- Understanding what happened in a past run

This project provides a **central logging setup** that can write to the **UI console**, so users can see messages directly in the application

---

## Design goals

The logging system is designed to:

- Feed logs into the **GUI console** for live feedback
- Make it easy to **add** logging to user defined methods and classes
- Enables logging by default on Data, DataProcessor, and Worker Core classes

Conceptually, there are three main pieces:

1. A shared logging configuration and helpers
2. Pre-decorated framework components (especially worker cores)
3. Decorators you can use on your own code (plotters, custom methods, etc.)

---

## Plotters and other user code

Unlike workers, **plotters do not have a core class** that is pre-decorated.

This is an intentional design choice:

- Plotters can be very simple or very complex
- Users may want fine-grained control over what is logged and when

As a result:

> Plotters ***must be explicitly decorated*** by the user if they should participate in the logging system.

The same is true for any other user-defined methods or classes that you want to show up in the logs (and optionally in the UI console):

- Custom data processors not deriving from DataProcessorCore
- Helper functions
- Utility classes

By decorating them yourself, you decide:

- Which functions are logged
- At what level (info, debug, warning, error)
- How verbose the output should be

---

## Logging decorators

The utilities module exposes decorators that do the heavy lifting.  
Typical patterns include:

- A **function decorator** – logs entry and exit of a function, plus optional details.
- A **class decorator** – automatically decorates every (or selected) method of a class.

At a conceptual level, usage looks like this:

```python
from utils.logging import with_logging, decorate_class_with_logging

@with_logging
def my_helper_function(...):
    # your helper logic here
    ...

@decorate_class_with_logging
class MyCustomPlotter:
    def draw_plot(self, ...):
```

Summary:

Decorators are provided to decorate classes ```@decorate_class_with_logging``` and functions ```@with_logging```.
Cores come pre-decorated with logging, and their messages go to the UI console without extra effort.
Plotters, and any other user-defined components, must be decorated explicitly to participate in the logging ecosystem.
The logging utilities make it easy to track the execution of your code in a consistent way, providing a unified view of the system’s behaviour.

By using the logging system thoughtfully, you get a transparent, traceable view of your data analysis runs, from dataset-driven configuration through to final plots.