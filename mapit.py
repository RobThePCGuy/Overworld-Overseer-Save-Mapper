import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
import sys
import re
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_save_files(saves_dir: Path):
    """Return a list of all JSON save files in the given directory."""
    return list(saves_dir.glob("*.json"))

def display_save_files(save_files: list[Path]):
    """Print a list of available save files and option for custom path."""
    print("\nAvailable Save Files:")
    for i, f in enumerate(save_files, 1):
        print(f"{i}. {f.stem}")
    print(f"{len(save_files) + 1}. Enter a custom file path")

def get_user_choice(num_options: int) -> int:
    """Prompt the user to choose a file number or a custom path."""
    while True:
        choice = input(f"\nEnter the number of the file to render (1-{num_options}): ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= num_options:
                return choice
        print(f"Please enter a valid number between 1 and {num_options}.")

def get_custom_path() -> Path:
    """Prompt the user for a custom JSON file path and validate it."""
    while True:
        custom_path = input("Enter the full path to the JSON file: ").strip('"\'')
        path = Path(custom_path)
        if path.is_file() and path.suffix.lower() == '.json':
            return path
        print("Invalid file path or not a JSON file. Please try again.")

def load_map_data(file_path: Path) -> list[dict]:
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("Map", [])
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from file: {file_path}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred while loading the file: {e}")
        sys.exit(1)

def format_descriptor_id(descriptor_id: str) -> str:
    """Insert a space before capital letters and title case the result."""
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', descriptor_id).title()

def create_color_mapping(map_df: pd.DataFrame, config: dict = None):
    """Create color mapping for descriptors, optionally using a config."""
    custom_colors = config.get('custom_colors', {}) if config else {}
    custom_labels = config.get('custom_labels', {}) if config else {}

    unique_desc = map_df['DescriptorID'].unique()
    
    formatted = pd.DataFrame({
        'DescriptorID': unique_desc,
        'FormattedDescriptorID': [
            custom_labels.get(d, format_descriptor_id(d)) for d in unique_desc
        ]
    })

    # Assign colors with custom colors taking precedence
    cmap = plt.get_cmap('tab20', len(unique_desc))
    descriptor_colors = {
        d: custom_colors.get(d, mcolors.rgb2hex(cmap(i % cmap.N)[:3]))
        for i, d in enumerate(unique_desc)
    }

    return descriptor_colors, formatted

def generate_map_html(map_df: pd.DataFrame, descriptor_colors: dict, x_min: int, x_max: int, y_min: int, y_max: int) -> str:
    html_map = ['<div class="map-grid">']
    for y in reversed(range(y_min, y_max + 1)):
        for x in range(x_min, x_max + 1):
            cell = map_df[(map_df["X"] == x) & (map_df["Y"] == y)]
            if not cell.empty:
                desc = cell.iloc[0]["DescriptorID"]
                html_map.append(
                    f'<div class="map-cell" data-descriptor="{desc}" data-x="{x}" data-y="{y}" '
                    f'title="({x}, {y})" style="background-color: {descriptor_colors[desc]};"></div>'
                )
            else:
                html_map.append(
                    f'<div class="map-cell empty" data-x="{x}" data-y="{y}" title="({x}, {y})"></div>'
                )
    html_map.append('</div>')
    return "\n".join(html_map)

def generate_html(descriptor_colors: dict, formatted_descriptors: pd.DataFrame, map_html: str, output_html: Path, grid_height: int, grid_width: int):
    legend_items = "\n".join(
        f'<div class="legend-item" data-descriptor="{row["DescriptorID"]}">'
        f'<span class="legend-color" style="background-color: {descriptor_colors[row["DescriptorID"]]}"></span>'
        f'<span class="legend-label">{row["FormattedDescriptorID"]}</span></div>'
        for _, row in formatted_descriptors.iterrows()
    )

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Underworld Overseer Save Map Visualization</title>
    <style>
        body {{
            font-family: Arial, sans-serif; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; background-color: #f0f0f0;
        }}
        h1 {{
            margin: 20px 0;
        }}
        .container {{
            display: flex; flex-direction: row; align-items: flex-start; margin-bottom: 20px; width: 90%;
            flex-wrap: wrap;
        }}
        .map-grid {{
            display: grid; 
            grid-template-rows: repeat({grid_height}, 20px); 
            grid-template-columns: repeat({grid_width}, 20px); 
            gap: 1px; 
            background-color: #333; 
            border: 2px solid #333;
            overflow: auto;
            max-height: 80vh;
            max-width: 80vw;
        }}
        .map-cell {{
            width: 20px; 
            height: 20px; 
            box-sizing: border-box; 
            transition: opacity 0.3s; 
            border: 1px solid #ccc;
            cursor: pointer;
        }}
        .map-cell.empty {{
            background-color: #fff;
        }}
        .legend {{
            margin-left: 20px; 
            display: flex; 
            flex-direction: column;
            max-height: 80vh;
            overflow-y: auto;
        }}
        .legend h2 {{
            margin-bottom: 10px;
        }}
        .legend-item {{
            display: flex; 
            align-items: center; 
            margin-bottom: 10px; 
            cursor: pointer; 
            transition: transform 0.2s;
        }}
        .legend-item:hover {{
            transform: scale(1.05);
        }}
        .legend-color {{
            width: 20px; 
            height: 20px; 
            margin-right: 10px; 
            border: 1px solid #000;
        }}
        .highlight {{
            opacity: 1 !important;
            transform: scale(1.2);
        }}
        .dimmed {{
            opacity: 0.2;
        }}
        .legend-item.active {{
            background-color: #e0e0e0;
            border: 2px solid #000;
            transform: scale(1.1);
            transition: transform 0.2s;
        }}
        /* Search Bar */
        .search-bar {{
            margin: 20px 0;
            width: 90%;
            max-width: 400px;
            display: flex;
        }}
        .search-bar input {{
            flex: 1;
            padding: 10px;
            border: 2px solid #ccc;
            border-radius: 4px 0 0 4px;
            outline: none;
        }}
        .search-bar button {{
            padding: 10px;
            border: 2px solid #ccc;
            border-left: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            border-radius: 0 4px 4px 0;
        }}
        .search-bar button:hover {{
            background-color: #45a049;
        }}
    </style>
</head>
<body>
    <h1>Game Map - Underworld Overseer</h1>
    <div class="search-bar">
        <input type="text" id="searchInput" placeholder="Search Descriptor...">
        <button onclick="searchDescriptor()">Search</button>
    </div>
    <div class="container">
        {map_html}
        <div class="legend">
            <h2>Legend</h2>
            {legend_items}
        </div>
    </div>
<script>
    const legendItems = document.querySelectorAll('.legend-item');
    const mapCells = document.querySelectorAll('.map-cell');
    let activeDescriptor = null;

    function highlightDescriptor(descriptor) {{
        legendItems.forEach(i => i.classList.toggle('active', i.getAttribute('data-descriptor') === descriptor));
        mapCells.forEach(c => {{
            if (c.getAttribute('data-descriptor') === descriptor) {{
                c.classList.add('highlight');
                c.classList.remove('dimmed');
            }} else {{
                c.classList.add('dimmed');
                c.classList.remove('highlight');
            }}
        }});
        activeDescriptor = descriptor;
    }}

    function clearHighlight() {{
        legendItems.forEach(i => i.classList.remove('active'));
        mapCells.forEach(c => c.classList.remove('dimmed', 'highlight'));
        activeDescriptor = null;
    }}

    legendItems.forEach(item => {{
        item.addEventListener('click', () => {{
            const descriptor = item.getAttribute('data-descriptor');
            activeDescriptor === descriptor ? clearHighlight() : highlightDescriptor(descriptor);
        }});
    }});

    mapCells.forEach(cell => {{
        cell.addEventListener('click', () => {{
            const descriptor = cell.getAttribute('data-descriptor');
            if (descriptor) {{
                activeDescriptor === descriptor ? clearHighlight() : highlightDescriptor(descriptor);
            }}
        }});
    }});

    function searchDescriptor() {{
        const query = document.getElementById('searchInput').value.trim();
        if (!query) return;
        const descriptor = Array.from(legendItems).find(item => item.querySelector('.legend-label').textContent.toLowerCase() === query.toLowerCase());
        if (descriptor) {{
            highlightDescriptor(descriptor.getAttribute('data-descriptor'));
            // Scroll to the descriptor in the legend
            descriptor.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
        }} else {{
            alert('Descriptor not found!');
        }}
    }}
</script>
</body>
</html>
"""
    with output_html.open("w", encoding='utf-8') as html_file:
        html_file.write(html_content)

def load_config(config_path: Path) -> dict:
    """Load configuration from a JSON file if provided."""
    if config_path and config_path.is_file():
        try:
            with config_path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from config file: {config_path}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"An error occurred while loading the config file: {e}")
            sys.exit(1)
    return {}

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Underworld Overseer Save Map Visualization Tool")
    parser.add_argument('-s', '--saves_dir', type=str, help='Path to the saves directory')
    parser.add_argument('-o', '--output', type=str, help='Path for the output HTML file')
    parser.add_argument('-c', '--config', type=str, help='Path to the JSON config file for colors and labels')
    return parser.parse_args()

def main():
    """Main entry point of the script."""
    args = parse_arguments()

    # Set default saves directory if not provided
    base_path = Path(args.saves_dir) if args.saves_dir else Path.home() / "AppData" / "LocalLow" / "MyronSoftware" / "UnderworldOverseer" / "Saves"
    if not base_path.exists():
        logging.error(f"The saves directory does not exist: {base_path}")
        sys.exit(1)

    save_files = get_save_files(base_path)

    if save_files:
        display_save_files(save_files)
        user_choice = get_user_choice(len(save_files) + 1)
        selected_file = save_files[user_choice - 1] if user_choice <= len(save_files) else get_custom_path()
    else:
        logging.warning("No JSON save files found in the default saves directory.")
        selected_file = get_custom_path()

    logging.info(f"Loading map from: {selected_file}")

    map_data = load_map_data(selected_file)
    if not map_data:
        logging.error("No map data found in the selected JSON file.")
        sys.exit(1)

    map_df = pd.DataFrame(map_data)
    x_min, x_max = map_df["X"].min(), map_df["X"].max()
    y_min, y_max = map_df["Y"].min(), map_df["Y"].max()
    grid_width = x_max - x_min + 1
    grid_height = y_max - y_min + 1

    # Load config if provided
    config = load_config(Path(args.config)) if args.config else None
    descriptor_colors, formatted_descriptors = create_color_mapping(map_df, config)

    logging.info("Generating map HTML...")
    map_html = generate_map_html(map_df, descriptor_colors, x_min, x_max, y_min, y_max)

    # Determine output HTML path
    output_html = Path(args.output) if args.output else (Path(__file__).parent / f"{selected_file.stem}.html" if '__file__' in globals() else Path.cwd() / f"{selected_file.stem}.html")

    generate_html(descriptor_colors, formatted_descriptors, map_html, output_html, grid_height, grid_width)
    logging.info(f"Map visualization saved as '{output_html}'. Open this file in a browser to view the interactive map.")

if __name__ == "__main__":
    main()
