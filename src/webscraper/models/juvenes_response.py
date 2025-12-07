# Schema to validate API response
SCHEMA = {
    "type": "array",
    "items": {"$ref": "#/$defs/toplevel"},
    "$defs": {
        "toplevel": {
            "required": ["menuTypes"],
            "properties": {
                "menuTypes": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/menuTypes"}
                }
            }
        },
        "menuTypes": {
            "required": ["menus"],
            "properties": {
                "menus": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/menus"}
                }
            }
        },
        "menus": {
            "required": ["menuName", "days"],
            "properties": {
                "days": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/days"}
                }
            }
        },
        "days": {
            "required": ["date", "mealoptions"],
            "properties": {
                "mealoptions": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/mealoptions"}
                }
            }
        },
        "mealoptions": {
            "required": ["name", "menuItems"],
            "properties": {
                "menuItems": {
                    "type": "array",
                    "items": {"$ref": "#/$defs/menuItems"}
                }
            }
        },
        "menuItems": {
            "required": ["name", "diets", "ingredients"]
        }
    }
}
