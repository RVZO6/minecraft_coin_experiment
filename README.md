# Minecraft Coin Data Pack & Resource Pack

This project adds custom **Gold Coins** and **Enchanted Gold Coins** to Minecraft vanilla loot tables using a Data Pack and Resource Pack.

## Project Structure
*   `resource_pack/`: The Resource Pack (Textures, Models).
*   `data_pack/`: The Data Pack (Loot tables).
*   `generate_data_pack.py`: Python script to generate the loot tables by injecting coin pools into vanilla tables.
*   `vanilla/`: Contains vanilla Minecraft data (cloned from `misode/mcmeta`) used as a base.

## Setup & Build

1.  **Requirements**: Python 3.
2.  **Generate Data Pack**:
    Run the generation script. It will automatically download vanilla assets if missing.
    ```bash
    python3 generate_data_pack.py
    ```
3.  **Install**:
    *   Copy `resource_pack` to your `.minecraft/resourcepacks` folder.
    *   Copy `data_pack` to your world's `datapacks` folder.

## Features
*   **Gold Coin**: Uncommon item found in many chests. yellow text.
*   **Enchanted Gold Coin**: Epic rarity item found only in rare structures (Strongholds, Ancient Cities, etc.). Purple text + Glint.

## Customization
Edit `generate_data_pack.py` to adjust:
*   `coin_weight`: How often standard coins appear.
*   `RARE_TABLES`: Which loot tables contain the Enchanted Coin.
