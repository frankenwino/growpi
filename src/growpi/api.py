from fastapi import FastAPI
from sensors.am2301 import AM2301
from main import load_sensors_from_config

app = FastAPI()

sensors = load_sensors_from_config()

# @app.get("/am2301")
# def get_am2301_reading():
#     """Fetch temperature and humidity from the AM2301 sensor."""
#     return "Hi" #AM2301.read()


@app.get("/")
def root():
    """Root endpoint to check if the API is running."""
    return {"message": "GrowPi API is running"}


@app.get("/sensors")
def list_sensors():
    """List all available sensors and their types."""
    return {"available_sensors": [sensor.__class__.__name__ for sensor in sensors]}


@app.get("/sensor/{sensor_name}")
def get_sensor_reading(sensor_name: str):
    """Fetch data from a specific sensor by name."""
    for sensor in sensors:
        if sensor.__class__.__name__.lower() == sensor_name.lower():
            return sensor.read_data()

    return {"error": f"Sensor '{sensor_name}' not found"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
