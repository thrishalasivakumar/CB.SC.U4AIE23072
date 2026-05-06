from logging_middleware.logger import Log

def schedule_tasks(vehicles, max_hours):

    n = len(vehicles)
    dp = [[0] * (max_hours + 1) for _ in range(n + 1)]

    Log(
        "backend",
        "info",
        "handler",
        f"Scheduling started for {n} vehicles"
    )

    for i in range(1, n + 1):

        duration = vehicles[i - 1]["Duration"]
        impact = vehicles[i - 1]["Impact"]

        for w in range(max_hours + 1):

            if duration <= w:
                dp[i][w] = max( impact + dp[i - 1][w - duration], dp[i - 1][w])

            else:
                dp[i][w] = dp[i - 1][w]

    Log(
        "backend",
        "info",
        "handler",
        f"Scheduling completed with max impact {dp[n][max_hours]}"
    )

    return dp[n][max_hours]