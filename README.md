# Enhanced Advanced Device Monitor

This project is an advanced device monitoring application built with Python. It provides real-time visualization of CPU, Disk, Memory, and GPU usage through both circular progress bars and line charts.

## Features

- Real-time monitoring of CPU, Disk, Memory, and GPU usage
- Circular progress bars for quick visual representation
- Line charts for historical data visualization
- System information display
- Dark mode UI for better visibility
- Timestamp for last update

## Requirements

- Python 3.x
- psutil
- GPUtil
- customtkinter
- matplotlib
- numpy

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/enhanced-advanced-device-monitor.git
   ```

2. Navigate to the project directory:
   ```
   cd enhanced-advanced-device-monitor
   ```

3. Install the required packages:
   ```
   pip install psutil GPUtil customtkinter matplotlib numpy
   ```

## Usage

Run the script with Python:

```
python enhanced_advanced_device_monitor.py
```

The application window will open, displaying real-time system resource usage.

## UI Components

- **Left Panel**: Displays circular progress bars for CPU, Disk, Memory, and GPU usage, along with system information.
- **Right Panel**: Shows line charts for historical data of resource usage.
- **Bottom**: Displays a timestamp of the last update.

## Customization

You can customize the application by modifying the following:

- Window size: Adjust the `geometry` parameter in the `DeviceMonitor` class.
- Update intervals: Modify the `sleep` duration in the `update_stats` method and the `after` calls for various update methods.
- Colors: Change the color scheme by modifying the `colors` list in the `DeviceMonitor` class.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Thanks to the creators and maintainers of psutil, GPUtil, customtkinter, and matplotlib.
- Inspired by various system monitoring tools and the need for a customizable, visually appealing monitor.