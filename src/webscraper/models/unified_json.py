from dataclasses import dataclass


@dataclass
class IndividualMenu:
    food_name: str
    diets: str
    menu_type: str
    date: str
    # ingredients: str
    menu_uid: int
    lang: str


@dataclass
class RestaurantContainer:
    restaurant_name: str
    area: str
    menu_options: list[IndividualMenu]


@dataclass
class CityContainer:
    city_name: str
    restaurants: list[RestaurantContainer]
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
