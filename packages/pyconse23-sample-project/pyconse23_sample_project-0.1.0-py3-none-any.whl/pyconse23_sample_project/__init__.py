from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

import httpx
import plotille


STOCKHOLM_COORDINATES = (59.3293, 18.0686)


def get_weather_forecast(coordinates: tuple[float, float], user_agent: str) -> dict[str, Any]:
    endpoint = "https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={}&lon={}"
    return httpx.get(endpoint.format(*coordinates), headers={'User-Agent': user_agent}).json()


def parse_time(time_str: str) -> datetime:
    return datetime.fromisoformat(time_str).astimezone(ZoneInfo("Europe/Stockholm"))


def get_forecast_temperature(forecast_data: dict[str, Any]) -> tuple[list[datetime], list[float]]:
    timeseries = forecast_data["properties"]["timeseries"]
    time = [parse_time(entry["time"]) for entry in timeseries]
    temperature = [entry["data"]["instant"]["details"]["air_temperature"] for entry in timeseries]
    return time, temperature


def main() -> None:
    forecast = get_weather_forecast(STOCKHOLM_COORDINATES, "httpx/pyconse-2023-demo")
    time, temperature = get_forecast_temperature(forecast)

    plot = plotille.plot(
        X=time,
        Y=temperature,
        X_label="Time",
        Y_label="Air temp",
        width=80,
        height=10,
        x_min=time[0],
        x_max=time[8],  # Forecast up to 8 hours from now
    )
    print(f"{'Temperature forecast in Stockholm [°C]':^100s}")
    print(plot)


if __name__ == "__main__":
    main()
