from typing import List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class IndividualMenu:
    food_name: str
    diets: str
    date: str
    # ingredients: str
    menu_type: str
    menu_type_id: int
    # menu_id: int
    lang: str


@dataclass
class UnifiedJson:
    restaurant_name: str
    menu_options: List[IndividualMenu]


# example output:
# resulted_json = {'restaurant_name': 'newton',
#                  'menu_options': [
#                      {
#                      'menu_type': 'Lounas',
#                      'date': '11.2.2025',
#                      'menu_list': [
#                          {
#                          'food_name': 'Nakki',
#                          'diets': 'G, L'
#                          },
#                          {
#                          'food_name': 'Peruna',
#                          'diets': ''
#                          }
#                         ]
#                      },
#                      {
#                          'menu_type': 'Vege',
#                          ...
#                      }
#                     ]
#                  }
