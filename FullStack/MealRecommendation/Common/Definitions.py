from enum import Enum

# NOT NULL
# SIGN UP
class Gender(Enum):
    MALE = 0,
    FEMALE = 1

# NOT NULL
class BodyFat(Enum):
    LOW = 0,
    MEDIUM = 1,
    HIGH = 2

# NOT NULL
# SIGN UP
class Goal(Enum):
    LOSE_WEIGHT = 0,
    MAINTAIN_WEIGHT = 1,
    BUILD_MUSCLE = 2

# NOT NULL
# SIGN UP
class ActivityLevel(Enum):
    SEDENTARY = 0,
    LIGHTLY_ACTIVE = 1,
    MODERATELY_ACTIVE = 2,
    VERY_ACTIVE = 3,
    EXTRA_ACTIVE = 4

# NOT NULL
# SIGN UP
# Can be one of them
class DietType(Enum):
    ANYTHING = 0,
    KETO = 1,
    VEGETERIAN = 2,
    VEGAN = 3,
    PALEO = 4,
    MEDITERRANEAN = 5

# NULLABLE
# SIGN UP

# Can be more than one
class Allergy(Enum):
    GLUTEN = 0,
    PEANUTS = 1,
    EGGS = 2,
    FISH = 3,
    SHELLFISH = 4,
    TREE_NUTS = 5,
    SOY = 6,
    DAIRY = 7


class Dataset(Enum):
    INGREDIENTS = 0,
    INTERACTIONS = 1,
    MEALS = 2,
    USERS = 3,
    RAW_MEALS = 4,
    RAW_INTERACTIONS = 5,


