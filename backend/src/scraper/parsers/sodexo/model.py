import msgspec


class SodexoMeta(msgspec.Struct):
    generated_timestamp: int
    ref_url: str
    ref_title: str
    restaurant_mashie_id: str


class AdditionalDietInfo(msgspec.Struct):
    dietcodeImages: list[str] | None = None
    allergens: str | None = None
    allergens_en: str | None = None
    allergens_fi: str | None = None


class RecipeItem(msgspec.Struct):
    name: str | None = None
    ingredients: str | list[str | None] | None = None
    nutrients: str | None = None
    dietcodes: str | None = None


class Courses(msgspec.Struct):
    title_fi: str
    title_en: str
    category: str
    meal_category: str | None = None
    dietcodes: str | None = None
    properties: str | None = None
    additionalDietInfo: AdditionalDietInfo | None = None
    price: str | None = None
    recipes: dict[str, RecipeItem] = msgspec.field(default_factory=dict)


class MealDates(msgspec.Struct):
    date: str
    courses: dict[str, Courses]


class SodexoModel(msgspec.Struct):
    meta: SodexoMeta
    timeperiod: str
    mealdates: list[MealDates]
