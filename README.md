# Underworld Overseer Save Mapper

[![Project Status](https://img.shields.io/badge/Status-Beta-orange)](https://www.repostatus.org/#beta)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Description

This tool visualizes save files from the game **Underworld Overseer** as interactive HTML maps. It allows you to:

*   **View your dungeon layout:** See the rooms, paths, and features of your Underworld Overseer save in a web browser.
*   **Customize appearance:**  Adjust colors for different map elements via a legend in the HTML output.
*   **Search and highlight:**  Quickly find specific map features (like "Heart Center" or "Secret Basement") using the search bar.
*   **Zoom and pan:** Easily navigate large maps using zoom controls and scrolling.
*   **Dark mode:**  Switch between light and dark themes for comfortable viewing.

This mapper is useful for:

*   **Planning your dungeon layout.**
*   **Sharing your dungeon progress with others.**
*   **Analyzing game mechanics and map generation.**

## Installation (For running from source - Python required)

If you want to run the script directly (Python is needed), follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/RobThePCGuy/Underworld-Overseer-Save-Mapper.git
    cd Underworld-Overseer-Save-Mapper
    ```

2.  **Install required Python packages:**
    ```bash
    pip install pandas matplotlib pathlib
    ```

## Usage

1.  **Run the script:** Execute the `main.py` script:
    ```bash
    python main.py
    ```

2.  **Select a save file:** The script will list available Underworld Overseer save files from the default saves directory.
    *   Choose a save file by entering its number.
    *   Alternatively, you can enter a custom file path to a `.json` save file.

3.  **Open the HTML map:** After processing, the script will generate an HTML file (e.g., `Besieged.html`) in the same directory as `main.py`. Open this HTML file in your web browser (Chrome, Firefox, etc.) to view the interactive map.

## Usage (Running the Executable - No Python needed)

1.  **Download the Executable:** Download the the .exe from
2.  **Run the Executable:**  Place the app exe in a convenient location and run it.
3.  **Follow on-screen instructions:** The executable will guide you through selecting a save file and generating the HTML map.

## Configuration

*   **`CONFIG_CUSTOM_COLORS` and `CONFIG_CUSTOM_LABELS`:** You can customize the colors and labels of map elements by editing these dictionaries in the `main.py` script before generating the EXE or running from source.

##  License

This project is licensed under the [MIT License](LICENSE) - see the `LICENSE` file for details.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your enhancements or bug fixes.

## Issues and Feature Requests

If you encounter any issues or have suggestions for new features, please open an issue on the [GitHub issue tracker]([link to your repo's issues]).

## Acknowledgements

*   This tool was inspired by and built for the game **Underworld Overseer** by Myron Software.
*   Uses [pandas](https://pandas.pydata.org/), [matplotlib](https://matplotlib.org/), and [PyInstaller](https://pyinstaller.org/).