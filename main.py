import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
import sys
import os
import re
import argparse
import logging
from typing import List, Dict, Tuple, Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# --- Configuration Constants ---
CONFIG_CUSTOM_COLORS = {
    "obsidian": "#120014",
    "stone": "#3b3a3a",
    "heart": "#FF0000",
    "claimed": "#0d9753",
    "enemyPath": "#f0f0f0",
    "stairs": "#FFFFFF",
    "gold": "#FFD700",
    "secretstonecarved": "#FFFF00",
    "secretbasement": "#A9A9A9",
    "infinitemine": "#D8BFD8",
}

CONFIG_CUSTOM_LABELS = {
    "enemypath": "Enemy Path",
    "hornethive": "Hornet Hive",
    "secretbasement": "Secret Basement",
    "waterbridge": "Water Bridge",
    "beetlenest": "Beetle Nest",
    "factorybubble": "Bubble Factory",
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
    "secretstonesewer": "Secret Stone Sewer",
}

DEFAULT_COLORS = {
    "custom_colors": CONFIG_CUSTOM_COLORS,
    "custom_labels": CONFIG_CUSTOM_LABELS,
}
# --- End of Configuration Constants ---


def get_save_files(saves_dir: Path) -> List[Path]:
    return list(saves_dir.glob("*.json"))


def display_save_files(save_files: List[Path]) -> None:
    print("\nAvailable Save Files:")
    for i, file_path in enumerate(save_files, 1):
        print(f"{i}. {file_path.stem}")
    print(f"{len(save_files) + 1}. Enter a custom file path")


def get_user_choice(num_options: int) -> int:
    while True:
        choice_str = input(
            f"\nEnter the number of the file to render (1-{num_options}): "
        ).strip()
        if choice_str.isdigit() and choice_str:
            choice = int(choice_str)
            if 1 <= choice <= num_options:
                return choice
        print(f"Please enter a valid number between 1 and {num_options}.")


def get_custom_file_path() -> Path:
    while True:
        custom_path_str = input("Enter the full path to the JSON file: ").strip("\"'")
        custom_path = Path(custom_path_str)
        if custom_path.is_file() and custom_path.suffix.lower() == ".json":
            return custom_path
        print("Invalid file path or not a JSON file. Please try again.")


def load_map_data(file_path: Path) -> List[Dict[str, Any]]:
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        map_data = data.get("Map", [])
        if not isinstance(map_data, list):
            logging.error(
                f"Expected 'Map' data to be a list, but got {type(map_data).__name__} in: {file_path}"
            )
            sys.exit(1)
        return map_data
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from file: {file_path}. {e}")
        sys.exit(1)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading {file_path}: {e}")
        sys.exit(1)


def format_descriptor_id(descriptor_id: str) -> str:
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", descriptor_id).title()


def create_color_mapping(map_df: pd.DataFrame) -> Tuple[Dict[str, str], pd.DataFrame]:
    custom_colors = DEFAULT_COLORS.get("custom_colors", {})
    custom_labels = DEFAULT_COLORS.get("custom_labels", {})

    unique_descriptors = map_df["DescriptorID"].unique()

    formatted_descriptors_df = pd.DataFrame(
        {
            "DescriptorID": unique_descriptors,
            "FormattedDescriptorID": [
                custom_labels.get(desc, format_descriptor_id(desc))
                for desc in unique_descriptors
            ],
        }
    )

    colormap = plt.get_cmap("tab20", len(unique_descriptors))
    descriptor_colors = {
        desc: custom_colors.get(desc, mcolors.rgb2hex(colormap(i % colormap.N)[:3]))
        for i, desc in enumerate(unique_descriptors)
    }

    return descriptor_colors, formatted_descriptors_df


def generate_map_html_optimized(
    map_df: pd.DataFrame,
    descriptor_colors: Dict[str, str],
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
) -> str:
    # Create a dictionary for fast lookup of cells by (Y, X) coordinates
    map_cell_dict = {(row["Y"], row["X"]): row for _, row in map_df.iterrows()}

    html_map_cells = []
    for y in reversed(range(y_min, y_max + 1)):
        for x in range(x_min, x_max + 1):
            cell_data = map_cell_dict.get((y, x))  # Efficient dictionary lookup
            if cell_data is not None:
                desc = cell_data["DescriptorID"]
                color = descriptor_colors[desc]
                html_map_cells.append(
                    f'<div class="map-cell" data-descriptor="{desc}" data-x="{x}" data-y="{y}" '
                    f'title="({x}, {y})" style="background-color: {color};"></div>'
                )
            else:
                html_map_cells.append(
                    f'<div class="map-cell empty" data-x="{x}" data-y="{y}" title="({x}, {y})"></div>'
                )
    return '<div class="map-grid">\n' + "\n".join(html_map_cells) + "\n</div>"


def generate_html(
    descriptor_colors: Dict[str, str],
    formatted_descriptors: pd.DataFrame,
    map_html: str,
    output_html: Path,
    grid_height: int,
    grid_width: int,
) -> None:
    legend_items_html = "\n".join(
        f'<div class="legend-item" data-descriptor="{row["DescriptorID"]}">\n'
        f'<span class="legend-color" style="background-color: {descriptor_colors[row["DescriptorID"]]}">\n</span>'
        f'<span class="legend-label">{row["FormattedDescriptorID"]}\n</span>'
        f'<input type="color" class="color-picker" data-descriptor="{row["DescriptorID"]}" value="{descriptor_colors[row["DescriptorID"]]}">\n'
        f"</div>"
        for _, row in formatted_descriptors.iterrows()
    )

    script_dir = Path(__file__).parent
    template_path = script_dir / "template.html"

    if not template_path.exists():
        logging.error(
            f"Template file 'template.html' not found in the script directory: {script_dir}"
        )
        sys.exit(1)

    with open(template_path, "r") as f:
        template = f.read()

    html_content = template.format(
        map_html=map_html,
        legend_items_html=legend_items_html,
        grid_height=grid_height,
        grid_width=grid_width,
    )

    with output_html.open("w", encoding="utf-8") as html_file:
        html_file.write(html_content)
    logging.info(f"Map visualization saved as '{output_html}'.")


def main() -> None:
    while True:
        saves_dir_path = (
            Path.home()
            / "AppData"
            / "LocalLow"
            / "MyronSoftware"
            / "UnderworldOverseer"
            / "Saves"
        )
        if not saves_dir_path.exists() or not saves_dir_path.is_dir():
            logging.error(
                f"Saves directory not found or is not a directory: {saves_dir_path}"
            )
            sys.exit(1)

        save_files = get_save_files(saves_dir_path)
        if save_files:
            display_save_files(save_files)
            user_choice = get_user_choice(len(save_files) + 1)
            selected_file_path = (
                save_files[user_choice - 1]
                if user_choice <= len(save_files)
                else get_custom_file_path()
            )

        else:
            logging.warning("No JSON save files found in the default saves directory.")
            selected_file_path = get_custom_file_path()

        logging.info(f"Loading map from: {selected_file_path}")

        map_data = load_map_data(selected_file_path)
        if not map_data:
            logging.error("No map data found in the selected JSON file.")
            sys.exit(1)

        map_df = pd.DataFrame(map_data)
        if (
            map_df.empty
            or "X" not in map_df.columns
            or "Y" not in map_df.columns
            or "DescriptorID" not in map_df.columns
        ):
            logging.error(
                "Loaded map data is invalid or missing required columns ('X', 'Y', 'DescriptorID')."
            )
            sys.exit(1)

        x_min, x_max = map_df["X"].min(), map_df["X"].max()
        y_min, y_max = map_df["Y"].min(), map_df["Y"].max()
        grid_width = x_max - x_min + 1
        grid_height = y_max - y_min + 1

        descriptor_colors, formatted_descriptors = create_color_mapping(map_df)

        logging.info("Generating map HTML...")
        # Use the optimized function
        map_html = generate_map_html_optimized(
            map_df, descriptor_colors, x_min, x_max, y_min, y_max
        )
        script_dir = Path(__file__).parent
        output_file_path = Path(script_dir / f"{selected_file_path.stem}.html")

        generate_html(
            descriptor_colors,
            formatted_descriptors,
            map_html,
            output_file_path,
            grid_height,
            grid_width,
        )

        while True:
            another_map = input("\nGenerate another map? (y/n): ").strip().lower()
            if another_map in ("y", "n"):
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        if another_map == "n":
            break

    print("\nProgram finished. Press Enter to exit.")
    input()


if __name__ == "__main__":
    main()