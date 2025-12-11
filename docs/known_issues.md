# Known Issues

For Python 3.10 the specific version of PyQt5 triggers a deprecation warning. This does not affect functionality and can be safely ignored.

## Matplotlib backends and threading
X-LAB Plotting Manager uses PyQt for its GUI and executes plotters inside worker threads.
Because PyQt is imported before Matplotlib, the QtAgg backend becomes active and cannot be changed within the same process.

As a result:
* Matplotlib cannot open interactive windows inside worker threads
* Calling plt.show() inside a processor or plotter will freeze or crash the application
* Backends such as TkAgg cannot be activated, because QtAgg is already running
* Only non-interactive backends (e.g. "Agg") are safe inside workers

✔ What implementation packages must do

```python
import matplotlib
matplotlib.use("Agg")  # safe for worker threads

...

fig.savefig("output.png")  # save plots to files
```
If interactivity is crucial, consider using Plotly instead for interactive plots.
