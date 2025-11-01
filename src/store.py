"""
Store - In-game store for purchasing random prizes with coins
"""
import json
import random
import os
from typing import List, Dict


class Store:
    """
    Manages the in-game store where players can spend coins on random prizes.
    """
    
    # Available prizes with their descriptions
    PRIZES = [
        "Golden Apple",
        "Speed Boost",
        "Extra Life",
        "Rainbow Skin",
        "Star Badge",
        "Mystery Box",
        "Lucky Charm",
        "Power Up",
        "Treasure Chest",
        "Magic Potion"
    ]
    
    def __init__(self, state_file: str = "store_state.json"):
        """
        Initialize the store.
        
        Args:
            state_file: Path to JSON file for persisting inventory
        """
        self.state_file = state_file
        self.inventory = self._load_inventory()
    
    def _load_inventory(self) -> List[str]:
        """Load inventory from file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    return data.get('inventory', [])
            except:
                return []
        return []
    
    def save_inventory(self):
        """Save current inventory to file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump({'inventory': self.inventory}, f, indent=2)
        except Exception as e:
            print(f"Error saving inventory: {e}")
    
    def purchase_item(self, coin_cost: int = 20) -> str:
        """
        Purchase a random prize from the store.
        
        Args:
            coin_cost: Cost of the item (default 20 coins)
            
        Returns:
            Name of the purchased item
        """
        # Select random prize
        prize = random.choice(self.PRIZES)
        
        # Add to inventory
        self.inventory.append(prize)
        
        # Save inventory
        self.save_inventory()
        
        return prize
    
    def get_inventory(self) -> List[str]:
        """Get current inventory."""
        return self.inventory.copy()
    
    def get_inventory_summary(self) -> Dict[str, int]:
        """
        Get inventory summary with item counts.
        
        Returns:
            Dictionary mapping item names to counts
        """
        summary = {}
        for item in self.inventory:
            summary[item] = summary.get(item, 0) + 1
        return summary
    
    def get_inventory_count(self) -> int:
        """Get total number of items in inventory."""
        return len(self.inventory)
