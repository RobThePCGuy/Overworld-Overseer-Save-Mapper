import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
import sys
import re

def get_save_files(saves_dir):
    return list(saves_dir.glob("*.json"))

def display_save_files(save_files):
    print("\nAvailable Save Files:")
    for i, f in enumerate(save_files, 1):
        print(f"{i}. {f.stem}")
    print(f"{len(save_files)+1}. Enter a custom file path")

def get_user_choice(num_options):
    while True:
        choice = input(f"\nEnter the number of the file to render (1-{num_options}): ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= num_options:
                return choice
        print(f"Please enter a valid number between 1 and {num_options}.")

def get_custom_path():
    while True:
        custom_path = input("Enter the full path to the JSON file: ").strip('"\'')
        path = Path(custom_path)
        if path.is_file() and path.suffix.lower() == '.json':
            return path
        print("Invalid file path or not a JSON file. Please try again.")

def load_map_data(file_path):
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("Map", [])
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        sys.exit(1)

def format_descriptor_id(descriptor_id):
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', descriptor_id).title()

def create_color_mapping(map_df):
    custom_colors = {
        'Abyss': '#0a0a0a',
        'Battlements': '#4b0082',
    }

    unique_desc = map_df['DescriptorID'].unique()
    formatted = pd.DataFrame({
        'DescriptorID': unique_desc,
        'FormattedDescriptorID': [format_descriptor_id(d) for d in unique_desc]
    })

    cmap = plt.get_cmap('tab20', len(unique_desc))
    color_list = [mcolors.rgb2hex(cmap(i % cmap.N)[:3]) for i in range(len(unique_desc))]

    descriptor_colors = {d: custom_colors.get(d, color_list.pop(0)) for d in unique_desc}
    return descriptor_colors, formatted

def generate_map_html(map_df, descriptor_colors, grid_height, grid_width):
    html_map = ['<div class="map-grid">']
    for y in reversed(range(grid_height)):
        for x in range(grid_width):
            cell = map_df[(map_df["X_adj"] == x) & (map_df["Y_adj"] == y)]
            if not cell.empty:
                desc = cell.iloc[0]["DescriptorID"]
                html_map.append(f'<div class="map-cell" data-descriptor="{desc}" style="background-color: {descriptor_colors[desc]};"></div>')
            else:
                html_map.append('<div class="map-cell empty"></div>')
    html_map.append('</div>')
    return "\n".join(html_map)

def generate_html(descriptor_colors, formatted_descriptors, map_html, output_html, grid_height, grid_width):
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
    <title>Game Map Visualization</title>
    <style>
        body {{
            font-family: Arial, sans-serif; margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; background-color: #f0f0f0;
        }}
        h1 {{
            margin: 20px 0;
        }}
        .container {{
            display: flex; flex-direction: row; align-items: flex-start; margin-bottom: 20px;
        }}
        .map-grid {{
            display: grid; grid-template-rows: repeat({grid_height}, 20px); grid-template-columns: repeat({grid_width}, 20px); gap: 1px; background-color: #333; border: 2px solid #333;
        }}
        .map-cell {{
            width: 20px; height: 20px; box-sizing: border-box; transition: opacity 0.3s; border: 1px solid #ccc;
        }}
        .map-cell.empty {{
            background-color: #fff;
        }}
        .legend {{
            margin-left: 20px; display: flex; flex-direction: column;
        }}
        .legend h2 {{
            margin-bottom: 10px;
        }}
        .legend-item {{
            display: flex; align-items: center; margin-bottom: 10px; cursor: pointer; transition: transform 0.2s;
        }}
        .legend-item:hover {{
            transform: scale(1.05);
        }}
        .legend-color {{
            width: 20px; height: 20px; margin-right: 10px; border: 1px solid #000;
        }}
        .highlight {{
            opacity: 1 !important;
        }}
        .dimmed {{
            opacity: 0.2;
        }}
    </style>
</head>
<body>
    <h1>Game Map - Underworld Overseer</h1>
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

        legendItems.forEach(item => {{
            item.addEventListener('click', () => {{
                const descriptor = item.getAttribute('data-descriptor');
                if (activeDescriptor === descriptor) {{
                    mapCells.forEach(cell => cell.classList.remove('dimmed', 'highlight'));
                    activeDescriptor = null;
                }} else {{
                    mapCells.forEach(cell => {{
                        if (cell.getAttribute('data-descriptor') === descriptor) {{
                            cell.classList.add('highlight');
                            cell.classList.remove('dimmed');
                        }} else {{
                            cell.classList.add('dimmed');
                            cell.classList.remove('highlight');
                        }}
                    }});
                    activeDescriptor = descriptor;
                }}
            }});
        }});
    </script>
</body>
</html>
"""
    with output_html.open("w", encoding='utf-8') as html_file:
        html_file.write(html_content)

def main():
    base_path = Path.home() / "AppData" / "LocalLow" / "MyronSoftware" / "UnderworldOverseer" / "Saves"
    if not base_path.exists():
        print(f"The saves directory does not exist: {base_path}")
        sys.exit(1)

    save_files = get_save_files(base_path)

    if save_files:
        display_save_files(save_files)
        user_choice = get_user_choice(len(save_files) + 1)
        selected_file = save_files[user_choice - 1] if user_choice <= len(save_files) else get_custom_path()
    else:
        print("No JSON save files found in the saves directory.")
        selected_file = get_custom_path()

    print(f"\nLoading map from: {selected_file}")

    map_data = load_map_data(selected_file)
    if not map_data:
        print("No map data found in the selected JSON file.")
        sys.exit(1)

    map_df = pd.DataFrame(map_data)
    map_df[['X_adj', 'Y_adj']] = map_df[['X', 'Y']] - map_df[['X', 'Y']].min()

    descriptor_colors, formatted_descriptors = create_color_mapping(map_df)
    grid_width = int(map_df["X_adj"].max() + 1)
    grid_height = int(map_df["Y_adj"].max() + 1)
    map_html = generate_map_html(map_df, descriptor_colors, grid_height, grid_width)

    output_html = selected_file.parent / "map_visualization.html"
    generate_html(descriptor_colors, formatted_descriptors, map_html, output_html, grid_height, grid_width)

    print(f"\nMap visualization saved as '{output_html}'. Open this file in a browser to view the interactive map.")

if __name__ == "__main__":
    main()
