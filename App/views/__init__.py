# blue prints are imported
# explicitly instead of using *
from .index_views import index_views
from .auth_views import auth_views
from .inventory_views import inventory_views
from .admin import setup_admin

views = [index_views, auth_views, inventory_views]
# blueprints must be added to this list
