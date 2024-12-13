# Underworld Overseer Map Mapper

>[!IMPORTANT]
> This is an **unofficial modification**. It is not supported by the developer, nor should you blame me or them if your toaster blows up. **Back up** the save file(s) before running the script.
>
> In order for the script to find a JSON save game, you must have started the level and selected `Save and Exit`. For each map that you `Save and Exit`, you will be able to select from the script's main menu.

## Features

- Scans the game save directory for JSON maps.
- The script parses the JSON map data from the saved game JSON file(s).
- Generates an accurate 2D grid of the level map.
- Includes a legend that lists all descriptors with their corresponding colors.
- Highlights grids per selection, dimming the rest.
- Find descriptos easily with the search bar.
- Uses a separate config file for changing colors and naming conventions.
- Includes a command line interface.

## Installation

1. Ensure you have Python 3.6 or later installed on your system. The script relies on several Python libraries, which can be installed using `pip`.

   ```bash
   pip install numpy pandas matplotlib
   ```

2. Clone this repository to your local machine:

   ```bash
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
        "hornethive": "Hornet Hive",
        "secretbasement": "Secret Basement",
        "waterbridge": "Water Bridge",
        "beetlenest": "Beetle Nest",
        "stonemine": "Stone Mine",
        "enemypathmonastery": "Enemy Path Monastery",
        "enemypathdesert": "Enemy Path Desert",
        "heartcenter": "Heart Center",
        "heartcenternofloor": "Heart Center No Floor",
        "infinitemine": "Infinite Gold Mine",
        "portalcenter": "Portal Center",
        "portalbonefairy": "Portal Bone Fairy",
        "portalbonefairycenter": "Portal Bone Fairy Center",
        "sapperpath": "Sapper Path",
        "guardpost": "Guard Post",
        "secretobsidiancarved": "Secret Obsidian Carved",
        "secretstonecarved": "Secret Stone Carved",
        "secretstonesewer": "Secret Stone Sewer"
    }
}
```

4. The script looks for JSON save files in the default directory:

    `~\AppData\LocalLow\MyronSoftware\UnderworldOverseer\Saves`

    You can choose a number that represents the save file to process, or you can enter a custom path.

5. After selecting a file, the script will process the map information and create an HTML file next to it.

6. To use the map, open it in your preferred web browser.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Support

For any issues or questions, please open an issue in the [GitHub repository](https://github.com/RobThePCGuy/Underworld-Overseer-Save-Mapper/issues).

*Happy mapping!*
