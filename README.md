# Underworld Overseer Map Visualization

>[!IMPORTANT]
> This is an **unofficial modification/cheat**. It is not supported by the developer, nor should you blame me or them if your toaster blows up.
>
> Use at your own risk. You should only attempt this if you understand what it does. If the terms `JSON parsing & data manipulation` do not make sense, just walk away.
>
> That being said, this will also show you hidden areas of a map, hence the cheat part. **Back up** the save file before running the script.
>
> In order for the script to find a JSON save game, you must have started the level and selected `Save and Exit`. For each map that you save and exit, you will be able to select from the script's main menu.

## Overview

The **Underworld Overseer Map Visualization** script is a Python tool designed to transform JSON save files from the game *Underworld Overseer* into interactive HTML map visualizations. By parsing the game's map data, the script generates a color-coded grid representing different map descriptors, allowing players and developers to easily visualize and analyze game maps.

## Features

- Scans the designated saves directory for available JSON save files.
- Parses and processes map data from JSON files, adjusting coordinates for accurate grid representation.
- Generates a grid representing the game map, with each cell colored according to its descriptor.
- Includes a sidebar listing all descriptors with their corresponding colors. Clicking on a legend item highlights all cells with that descriptor.
- Utilizes JavaScript to enable users to filter and highlight specific map areas by interacting with the legend.

## Installation

1. Ensure you have Python 3.6 or later installed on your system. The script relies on several Python libraries, which can be installed using `pip`.

   ```bash
   pip install numpy pandas matplotlib
   ```

2. Clone this repository to your local machine:

   ```cmd
   git clone https://github.com/RobThePCGuy/Underworld-Overseer-Save-Mapper.git
   cd Underworld-Overseer-Save-Mapper
   ```

3. Execute the script using Python:

   ```cmd
   python mapit.py
   ```

4. The script searches for JSON save files in the default directory:

   ```cmd
   ~\AppData\LocalLow\MyronSoftware\UnderworldOverseer\Saves
   ```

   - If your saves are stored elsewhere, you can provide a custom file path when prompted.

5. Choose one of the existing JSON save files. Enter the number corresponding to the desired file.
   - Optionally, you may enter a custom path.

6. After selecting a file, the script will process the map data and generate a `map_visualization.html` file in the same directory as the selected JSON file.

7. Open the generated HTML file in your preferred web browser to interact with the map visualization.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Support

For any issues or questions, please open an issue in the [GitHub repository](https://github.com/RobThePCGuy/Underworld-Overseer-Save-Mapper/issues).

*Happy mapping!*
