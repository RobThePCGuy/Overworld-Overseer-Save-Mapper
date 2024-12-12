# Underworld Overseer Map Visualization

>[!IMPORTANT]
> This is an **unofficial modification/cheat**. It is not supported by the developer, nor should you blame me or them if your toaster blows up.
>
> Use at your own risk. You should only attempt this if you understand what it does. If the terms `JSON parsing & data manipulation` do not make sense, just walk away.
>
> That being said, this will also show you hidden areas of a map, hence the cheat part. **Back up** the save file before running the script.
>
> In order for the script to find a JSON save game, you must have started the level and selected `Save and Exit`. For each map that you save and exit, you will be able to select from the script's main menu.

## Features

- Scans the designated saves directory for available JSON save files.
- Parses and processes map data from JSON files, adjusting coordinates for accurate grid representation.
- Generates a grid representing the game map, with each cell colored according to its descriptor.
- Shows an accurate grid x, y matching the JSON file exactly.
- Includes a sidebar listing all descriptors with their corresponding colors. Clicking on a legend item highlights all cells with that descriptor.
- Clicking an individual cell block also highlights and emboldens the matching legend descriptor.
- Utilizes JavaScript to enable users to search, filter, and highlight specific map areas by interacting with the legend.
- Uses a separate config file for changing colors and naming conventions.
- Includes a command line interface.

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

3. Run the Script:

   The following CLI will utilize the config file included in the repo, it will search for any save files, allow for selection, then output the HTML right next to the script.

     ```bash
     python mapit.py -c "config/colors.json"
     ```

     - `-s` or `--saves_dir`: Specify a custom saves directory.
     - `-o` or `--output`: Define a custom output HTML file path.
     - `-c` or `--config`: Provide a JSON configuration file for customizing colors and labels.

### Sample Configuration File (`config/colors.json`):

To utilize the configuration file for custom colors and labels, edit or create a `config/colors.json`.

```json
{
    "custom_colors": {
        "obsidian": "#120014",
        "stone": "#3b3a3a",
        "heart": "#FF0000",
        "claimed": "#0d9753",
        "enemyPath": "#f0f0f0",
        "stairs": "#FFFFFF",
        "gold": "#FFD700",
        "secretstonecarved": "#FFFF00",
        "secretbasement": "#A9A9A9",
        "infinitemine": "#D8BFD8"
    },
    "custom_labels": {
        "enemypath": "Enemy Path",
        "enemypathmonastery": "Enemy Path Monastery",
        "heartcenter": "Heart Center",
        "heartcenternofloor": "Heart Center No Floor",
        "infinitemine": "Infinite Gold Mine",
        "portalcenter": "Portal Center",
        "sapperpath": "Sapper Path",
        "secretstonesewer": "Secret Stone Sewer"
    }
}
```

4. The script searches for JSON save files in the default directory:

   ```cmd
   ~\AppData\LocalLow\MyronSoftware\UnderworldOverseer\Saves
   ```

   - If your saves are stored elsewhere, you can provide a custom file path when prompted.

5. Choose one of the existing JSON save files. Enter the number corresponding to the desired file.
   - Optionally, you may enter a custom path.

6. After selecting a file, the script will process the map data and generate an HTML file in the same directory as the script, named the same as the selected file.

7. Open the generated HTML file in your preferred web browser to interact with the map visualization.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Support

For any issues or questions, please open an issue in the [GitHub repository](https://github.com/RobThePCGuy/Underworld-Overseer-Save-Mapper/issues).

*Happy mapping!*
