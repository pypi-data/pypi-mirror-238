# pybrams

**pybrams** is a Python package that allows you to access information and data from the BRAMS (Belgian RAdio Meteor Stations) project. BRAMS is a network of radio receiving stations that use forward scattering techniques to study the meteoroid population. This project, coordinated by the Belgian Institute for Space Aeronomy (BISA), provides a valuable source of data for researchers, amateur astronomers, and meteor enthusiasts.

## Features

- Fetch detailed information about BRAMS stations, including their location, name, number of antennas, and more.
- Retrieve raw data files in WAV format, which can be used for in-depth analysis of meteoroid activity.
- Access PNG images representing spectrograms, making it easy to visualize meteoroid detections.

## Installation

You can install **pybrams** using pip:

pip install pybrams


## Usage

Here's a simple example of how to use **pybrams** to retrieve station information:

```python
from brams import locations
import json

for location in locations.all():

    json.dumps(location, indent = 4)
```

For more detailed usage instructions, documentation, and examples, please visit our documentation.
Get Started

Ready to explore the fascinating world of meteoroid detection and analysis? Install pybrams and start accessing BRAMS data with ease. Whether you're a scientist, amateur astronomer, or simply curious about meteoroid activity, this package provides the tools you need to delve into this exciting field.
Contribute

Contributions and feedback are welcome! If you'd like to improve this package or report issues, please visit our GitHub repository.
License

This package is licensed under the MIT License. Feel free to use and modify it as needed.
