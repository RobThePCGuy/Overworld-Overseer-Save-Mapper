# Underworld Overseer Map Visualization

## Overview

The **Underworld Overseer Map Visualization** script is a Python tool designed to transform JSON save files from the game *Underworld Overseer* into interactive HTML map visualizations. By parsing the game's map data, the script generates a color-coded grid representing different map descriptors, allowing players and developers to easily visualize and analyze game maps.

## Features

- **Automatic Save File Detection:** Scans the designated saves directory for available JSON save files.
- **User-Friendly Interface:** Provides a command-line interface for selecting existing save files or specifying custom file paths.
- **Data Processing:** Parses and processes map data from JSON files, adjusting coordinates for accurate grid representation.
- **Customizable Color Mapping:** Assigns unique colors to different map descriptors, with support for custom color definitions.
- **Interactive HTML Output:** Generates an HTML file featuring an interactive map grid and legend, enabling users to highlight specific map descriptors.
- **Error Handling:** Includes robust error handling for file operations and JSON parsing to ensure smooth execution.

## Installation

### Prerequisites

Ensure you have Python 3.6 or later installed on your system. The script relies on several Python libraries, which can be installed using `pip`.

### Dependencies

Install the required Python packages using the following command:

```bash
pip install numpy pandas matplotlib
```

### Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/RobThePCGuy/Underworld-Overseer-Save-Mapper.git
cd Underworld-Overseer-Save-Mapper
```

## Usage

1. **Locate Save Files:**

   The script searches for JSON save files in the default directory:
   
   ```
   C:\Users\<YourUsername>\AppData\LocalLow\MyronSoftware\UnderworldOverseer\Saves
   ```
   
   Ensure that your game save files are located in this directory. If your saves are stored elsewhere, you can provide a custom file path when prompted.

2. **Run the Script:**

   Execute the script using Python:

   ```bash
   python mapit.py
   ```

3. **Select a Save File:**

   - **Existing Files:** The script will list all available JSON save files. Enter the number corresponding to the desired file.
   - **Custom File Path:** If you prefer to use a different JSON file, select the option to enter a custom file path and provide the full path to your JSON file.

4. **Generate Visualization:**

   After selecting a file, the script will process the map data and generate an `map_visualization.html` file in the same directory as the selected JSON file.

5. **View the Map:**

   Open the generated HTML file in your preferred web browser to interact with the map visualization.

## How It Works

### Script Breakdown

The script is structured into several key functions, each responsible for a specific part of the process:

1. **Importing Libraries:**

   ```python
   import json
   import numpy as np
   import pandas as pd
   import matplotlib.pyplot as plt
   import matplotlib.colors as mcolors
   from pathlib import Path
   import sys
   import re
   ```

   These libraries handle JSON parsing, data manipulation, color mapping, file system interactions, and regular expressions.

2. **File Handling:**

   - **`get_save_files(saves_dir)`**
     
     Retrieves a list of all `.json` files in the specified saves directory.
   
   - **`display_save_files(save_files)`**
     
     Displays the available save files to the user for selection.
   
   - **`get_user_choice(num_options)`**
     
     Prompts the user to select a file by entering the corresponding number.
   
   - **`get_custom_path()`**
     
     Allows the user to input a custom file path if the desired file isn't listed.

3. **Data Loading and Processing:**

   - **`load_map_data(file_path)`**
     
     Loads and parses the "Map" data from the selected JSON file. Handles JSON decoding errors and other exceptions.
   
   - **`format_descriptor_id(descriptor_id)`**
     
     Formats descriptor IDs by inserting spaces between camelCase words and capitalizing them for better readability.
   
   - **`create_color_mapping(map_df)`**
     
     Assigns colors to each unique descriptor in the map data. Utilizes custom colors where defined and falls back to a color palette for others.
   
   - **`generate_map_html(map_df, descriptor_colors, grid_height, grid_width)`**
     
     Creates the HTML structure for the map grid, assigning background colors based on descriptors.

4. **HTML Generation:**

   - **`generate_html(descriptor_colors, formatted_descriptors, map_html, output_html, grid_height, grid_width)`**
     
     Compiles the complete HTML file, including styling, the map grid, legend, and interactivity through JavaScript. The legend allows users to highlight specific descriptors on the map.

5. **Main Execution Flow:**

   - **`main()`**
     
     Orchestrates the entire process:
     - Determines the saves directory.
     - Lists available save files and handles user selection.
     - Loads and processes map data.
     - Generates and saves the interactive HTML visualization.

6. **Script Entry Point:**

   ```python
   if __name__ == "__main__":
       main()
   ```

   Ensures that the `main()` function runs when the script is executed.

### HTML Output

The generated `map_visualization.html` includes:

- **Map Grid:** A grid representing the game map, with each cell colored according to its descriptor.
- **Legend:** A sidebar listing all descriptors with their corresponding colors. Clicking on a legend item highlights all cells with that descriptor.
- **Interactivity:** JavaScript enables users to filter and highlight specific map areas by interacting with the legend.

## Customization

- **Color Mapping:**

  You can customize the colors assigned to specific descriptors by modifying the `custom_colors` dictionary within the `create_color_mapping` function:

  ```python
  custom_colors = {
      'Abyss': '#0a0a0a',
      'Battlements': '#4b0082',
      # Add more custom descriptors and colors here
  }
  ```

- **Grid Size:**

  The script automatically adjusts the grid size based on the map data. However, you can modify the cell dimensions by editing the CSS styles within the `generate_html` function.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Support

For any issues or questions, please open an issue in the [GitHub repository](https://github.com/RobThePCGuy/Underworld-Overseer-Save-Mapper/issues).

---

*Happy mapping!*
