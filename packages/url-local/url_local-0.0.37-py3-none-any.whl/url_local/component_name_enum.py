from enum import Enum

# Order by a..z of component name
class ComponentName(Enum):
    AUTHENTICATION = "authentication"  # login
    EVENT = "event"
    GENDER_DETECTION = "gender-detection"
    GROUP = "group"
    GROUP_PROFILE = "group-profile"
    LOGGER = "logger"
    MARKETPLACE_GOODS = "marketplace-goods"
    STORAGE = "storage"
    TIMELINE = "timeline"
    USER_REGISTRATION = "user-registration"
    
