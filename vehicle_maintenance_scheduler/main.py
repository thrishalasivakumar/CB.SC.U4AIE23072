from vehicle_maintenance_scheduler.api_service import (get_depots,get_vehicles)
from logging_middleware.logger import Log
from vehicle_maintenance_scheduler.scheduler import schedule_tasks

def main():

    Log(
        "backend",
        "info",
        "route",
        "Vehicle maintenance scheduler started"
    )

    depots = get_depots()
    vehicles = get_vehicles()

    for depot in depots:

        depot_id = depot["ID"]
        hours = depot["MechanicHours"]

        Log(
            "backend",
            "info",
            "handler",
            f"Processing depot {depot_id}"
        )

        result = schedule_tasks(
            vehicles,
            hours
        )

        print(
            f"Depot {depot_id} -> "
            f"Maximum Impact: {result}"
        )

        Log(
            "backend",
            "info",
            "handler",
            f"Completed depot {depot_id}"
        )


if __name__ == "__main__":
    main()