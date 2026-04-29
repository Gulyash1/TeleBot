from .start_handler import rt
from .maintance import maintance_router
from .consumption import consumption_router
from .back_to_main import rt_to_main
from .server_stats_check import stats_router

all_routers = (rt, maintance_router, consumption_router, rt_to_main, stats_router)