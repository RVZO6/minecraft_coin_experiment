import json
import os

# ==========================================
#              CONFIGURATION
# ==========================================

# Pack format versions (use "major.minor" format, e.g. "94.1" -> [94, 1])
DATA_PACK_FORMAT = "94.1"
RESOURCE_PACK_FORMAT = "75.0"

# Paths - Base directory for ALL loot tables (not just chests)
VANILLA_DIR = "vanilla/data/minecraft/loot_table"
OUTPUT_DIR = "data_pack/data/minecraft/loot_table"


def parse_pack_format(version_str):
    """Parse a version string like '94.1' into [major, minor] list."""
    parts = version_str.split(".")
    if len(parts) == 2:
        return [int(parts[0]), int(parts[1])]
    elif len(parts) == 1:
        return [int(parts[0]), 0]
    else:
        raise ValueError(f"Invalid pack format: {version_str}")


# ==========================================
#              COIN DEFINITIONS
# ==========================================

COINS = {
    "gold_coin": {
        "name": "Gold Coin",
        "model": "coin_pack:coin",
        "rarity": "uncommon",
        "glint": False,
    },
    "enchanted_gold_coin": {
        "name": "Enchanted Gold Coin",
        "model": "coin_pack:coin",
        "rarity": "rare",
        "glint": True,
    },
}

# ==========================================
#              TIER DEFINITIONS
# ==========================================
# Define tiers with their coin drop settings.
# Each tier specifies which coins drop, their weights, count ranges, and drop chances.

TIERS = {
    "common": {
        "gold_coin": {
            "weight": 1,
            "count_min": 1,
            "count_max": 2,
            "chance": 0.3,  # 30% chance to roll this pool
        }
        # No enchanted coin in common tier
    },
    "adventure": {
        "gold_coin": {
            "weight": 1,
            "count_min": 2,
            "count_max": 4,
            "chance": 0.7,  # 70% chance
        },
        "enchanted_gold_coin": {
            "weight": 1,
            "count_min": 1,
            "count_max": 1,
            "chance": 0.005,  # 0.5% chance
        },
    },
    "treasure": {
        "gold_coin": {
            "weight": 1,
            "count_min": 3,
            "count_max": 8,
            "chance": 1.0,  # Always drops
        },
        "enchanted_gold_coin": {
            "weight": 1,
            "count_min": 1,
            "count_max": 1,
            "chance": 0.05,  # 5% chance
        },
    },
}

# ==========================================
#              LOOT TABLE ASSIGNMENTS
# ==========================================
# Assign each loot table to a tier.
# Path is relative to vanilla/data/minecraft/loot_table/
# You can add ANY loot table here (chests, fishing, entities, etc.)

LOOT_TABLES = {
    # ===== CHESTS - COMMON =====
    "chests/spawn_bonus_chest": "common",
    "chests/igloo_chest": "common",
    "chests/village/village_plains_house": "common",
    "chests/village/village_desert_house": "common",
    "chests/village/village_savanna_house": "common",
    "chests/village/village_snowy_house": "common",
    "chests/village/village_taiga_house": "common",
    "chests/village/village_armorer": "common",
    "chests/village/village_butcher": "common",
    "chests/village/village_cartographer": "common",
    "chests/village/village_fisher": "common",
    "chests/village/village_fletcher": "common",
    "chests/village/village_mason": "common",
    "chests/village/village_shepherd": "common",
    "chests/village/village_tannery": "common",
    "chests/village/village_temple": "common",
    "chests/village/village_toolsmith": "common",
    "chests/village/village_weaponsmith": "common",
    # ===== CHESTS - ADVENTURE =====
    "chests/simple_dungeon": "adventure",
    "chests/abandoned_mineshaft": "adventure",
    "chests/jungle_temple": "adventure",
    "chests/jungle_temple_dispenser": "adventure",
    "chests/pillager_outpost": "adventure",
    "chests/desert_pyramid": "adventure",
    "chests/woodland_mansion": "adventure",
    "chests/ruined_portal": "adventure",
    "chests/shipwreck_supply": "adventure",
    "chests/shipwreck_treasure": "adventure",
    "chests/nether_bridge": "adventure",
    "chests/underwater_ruin_big": "adventure",
    "chests/underwater_ruin_big": "adventure",
    "chests/underwater_ruin_small": "adventure",
    "chests/trial_chambers/reward_common": "adventure",
    "chests/trial_chambers/reward_rare": "adventure",
    "chests/trial_chambers/reward_unique": "adventure",
    "chests/trial_chambers/supply": "adventure",
    # ===== CHESTS - TREASURE =====
    "chests/stronghold_corridor": "treasure",
    "chests/stronghold_crossing": "treasure",
    "chests/stronghold_library": "treasure",
    "chests/end_city_treasure": "treasure",
    "chests/bastion_treasure": "treasure",
    "chests/bastion_bridge": "treasure",
    "chests/bastion_hoglin_stable": "treasure",
    "chests/bastion_other": "treasure",
    "chests/ancient_city": "treasure",
    "chests/ancient_city_ice_box": "treasure",
    "chests/ancient_city_ice_box": "treasure",
    "chests/buried_treasure": "treasure",
    "chests/buried_treasure": "treasure",
    "chests/trial_chambers/reward_ominous": "treasure",
    # ===== FISHING =====
    "gameplay/fishing/treasure": "adventure",
    # ===== ENTITIES =====
    # "entities/zombie":                "common",
}


# ==========================================
#              GENERATION LOGIC
# ==========================================


def build_coin_entry(coin_id, tier_config):
    """Build a loot table entry for a coin."""
    coin = COINS[coin_id]

    entry = {
        "type": "minecraft:item",
        "name": "minecraft:iron_nugget",
        "weight": tier_config["weight"],
        "functions": [
            {
                "function": "minecraft:set_name",
                "name": {"text": coin["name"], "italic": False},
            },
            {
                "function": "minecraft:set_components",
                "components": {
                    "minecraft:item_model": coin["model"],
                    "minecraft:rarity": coin["rarity"],
                },
            },
            {
                "function": "minecraft:set_count",
                "count": {
                    "min": tier_config["count_min"],
                    "max": tier_config["count_max"],
                },
            },
        ],
    }

    if coin["glint"]:
        entry["functions"][1]["components"]["minecraft:enchantment_glint_override"] = (
            True
        )

    return entry


def build_coin_pools(tier_name):
    """Build all coin pools for a tier. Each coin gets its own pool with its own chance."""
    if tier_name not in TIERS:
        return []

    pools = []
    tier = TIERS[tier_name]

    for coin_id, config in tier.items():
        pool = {
            "rolls": 1,
            "bonus_rolls": 0.0,
            "entries": [build_coin_entry(coin_id, config)],
        }

        # Add chance condition if not 100%
        if config["chance"] < 1.0:
            pool["conditions"] = [
                {"condition": "minecraft:random_chance", "chance": config["chance"]}
            ]

        pools.append(pool)

    return pools


def generate_tier_files():
    """Generate the distinct loot table files for each tier."""
    print("Generating tier loot tables...")
    base_dir = "data_pack/data/coin_pack/loot_table/tiers"
    os.makedirs(base_dir, exist_ok=True)

    for tier_name in TIERS:
        pools = build_coin_pools(tier_name)
        loot_table = {"type": "minecraft:chest", "pools": pools}

        path = os.path.join(base_dir, f"{tier_name}.json")
        with open(path, "w") as f:
            json.dump(loot_table, f, indent=2)
        print(f"  Generated {path}")


def setup_environment():
    """Ensure vanilla data and output directories exist."""
    if not os.path.exists("vanilla"):
        print("Vanilla data not found. Cloning from misode/mcmeta (data branch)...")
        os.system(
            "git clone --depth 1 --branch data https://github.com/misode/mcmeta.git vanilla"
        )

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Create pack.mcmeta if missing
    mcmeta_path = "data_pack/pack.mcmeta"
    # Always recreate/update pack.mcmeta to ensure consistency
    os.makedirs("data_pack", exist_ok=True)
    fmt = parse_pack_format(DATA_PACK_FORMAT)
    with open(mcmeta_path, "w") as f:
        json.dump(
            {
                "pack": {
                    "description": "Minecraft coin data pack.",
                    "pack_format": fmt[0],
                    "min_format": fmt,
                    "max_format": fmt,
                }
            },
            f,
            indent=4,
        )


def generate_data_pack():
    """Main generation function."""
    setup_environment()
    generate_tier_files()

    print(f"Processing {len(LOOT_TABLES)} loot tables...")

    for table_path, tier_name in LOOT_TABLES.items():
        # Find the vanilla file
        src_path = os.path.join(VANILLA_DIR, f"{table_path}.json")

        if not os.path.exists(src_path):
            print(f"  Warning: {table_path}.json not found, skipping.")
            continue

        # Load vanilla loot table
        with open(src_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"  Skipping {table_path}: Invalid JSON")
                continue

        # Inject a reference to the tier loot table
        # We append a single pool that rolls the tier loot table once.
        reference_pool = {
            "rolls": 1,
            "entries": [
                {
                    "type": "minecraft:loot_table",
                    "value": f"coin_pack:tiers/{tier_name}",
                }
            ],
        }

        if "pools" not in data:
            data["pools"] = []
        data["pools"].append(reference_pool)

        # Write modified loot table
        dest_path = os.path.join(OUTPUT_DIR, f"{table_path}.json")
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        with open(dest_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"  [{tier_name}] {table_path}.json")

    print("\nData Pack generated successfully!")


if __name__ == "__main__":
    generate_data_pack()
