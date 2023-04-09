import datetime
import math
import gps
import time
import random
import board
import numpy as np
import adafruit_ina219
#import robotics_library as rl

# define the function to check the state of the solar panels
def check_panel(panel_id):
    # get the current state of the solar panels
    panel_state = get_panel_state(panel_id)
    # check for any signs of damage or malfunction
    if panel_state == 'damaged':
        # send an alert or take corrective action
        send_alert(panel_id,'panel damage detected')
    elif panel_state == 'malfunction':
        # send an alert or take corrective action
        send_alert(panel_id,'panel malfunction detected')
    elif panel_state == 'normal':
        # if everything is normal ,then monitor the panel
        monitor_panel(panel_id)

# define the function to monitor the state of the solar panels
def monitor_panel(panel_id):
        collect_energy_data(panel_id)
        clean_panel(panel_id)


# define the function to clean the solar panels
def clean_panel():
    # perform the cleaning action
    # define the function to clean the solar panels
    # move the robotic arm to the panel location
    move_arm_to_panel()
    # activate the cleaning pad
    activate_cleaning_pad()
    # move the robotic arm to the next panel location
    move_arm_to_next_panel()

# define the function to move the robotic arm to the panel location
def move_arm_to_panel():
    # move the robotic arm to the location of the panel that needs to be cleaned
    # For example, you can use the robot's motor controls to move the arm to the desired location
    print("Moving robotic arm to panel location...")
    time.sleep(2)
    pass

# define the function to activate the cleaning pad
def activate_cleaning_pad():
    # activate the cleaning pad to clean the panel surface
    # For example, you can use a motor or a pneumatic system to activate the cleaning pad
    print("Activating cleaning pad...")
    time.sleep(1)
    pass

# define the function to move the robotic arm to the next panel location
def move_arm_to_next_panel():
    # move the robotic arm to the location of the next panel that needs to be cleaned
    # For example, you can use the robot's motor controls to move the arm to the next panel location
    print("Moving robotic arm to next panel location...")
    time.sleep(2)

    pass


# define the function to collect data on solar panel performance
def collect_data():
    #monitoring the weather conditions and air quality
    temperature = random.uniform(0, 100)  # simulate temperature data between 0 and 100 degrees Celsius
    humidity = random.uniform(0,100) #simulate humidity data between 0 and 100 percentage
    # Simulate reading from a gas sensor
    gas_concentration = random.uniform(0, 1)  # Random value between 0 and 1
    if gas_concentration < 0.1:
        air_quality = "Excellent"
    elif gas_concentration < 0.3:
        air_quality = "Good"
    elif gas_concentration < 0.7:
        air_quality = "Fair"
    elif gas_concentration < 1.0:
        air_quality =  "Poor"
    else:
        air_quality = "Unhealthy"

    if temperature > 80 :
        # if temperature is greater than 80 degrees Celsius, send alert
        send_alert("Environment", "Temperature is too high")
    elif gas_concentration > 0.3:
        #if gas concentration is above 0.3 , sends alert 
        print(air_quality)
        send_alert("Environment","Air Quality is not good")
    elif humidity > 30 :
        #if humidity is greater than 30 percent , sends alert , as it poors the working of the solar panel
        send_alert("Environment","Humidity is too high")
    else:
        #if temperature is less than 80 , gas concentration is less than 0.3 and humidity percentage is less than 30 then it returns good
        print("Air quality : ", air_quality)
        return "good"
    return "bad" 

# define the function to get the state of the solar panel
def get_panel_state():
    # get the state of the solar panel, power of panel is checked 
    # use sensors to measure the voltage and current from the panel
    # simulating random value of voltage and current
    voltage = random.uniform(0,5)#read_voltage(panel_id)
    current = random.uniform(0,10)#read_current(panel_id)
    power = voltage * current

    # define acceptable ranges for voltage, current, and power
    min_voltage = 0.5  # volts
    max_voltage = 5  # volts
    min_current = 0  # amps
    max_current = 10  # amps
    min_power = 0  # watts
    max_power = 50  # watts

    # check if readings fall outside acceptable ranges
    if voltage < min_voltage or voltage > max_voltage:
        send_alert(panel_id, "Voltage reading out of range")
        return "damaged"
    if current < min_current or current > max_current:
        send_alert(panel_id, "Current reading out of range")
        return "damaged"
    if power < min_power or power > max_power:
        send_alert(panel_id, "Power reading out of range")
        return "malfunction"
    else :
        return "normal"


# define the function to monitor the environment around the solar panel
def monitor_environment(panel_id):
    # monitor the environment around the solar panel, such as weather conditions and air quality
    #to measure temperature, humidity and air quality collect data function is used
    state = collect_data()
    if state == "good" :
        #if collect_data returns good , this implies it is a fine weather to monitor the solar panel , for which check panel function is called
        check_panel(panel_id)
    else :
        send_alert("Environment"," Weather conditions are not good to monitor the solar panels")

# define the function to collect energy data
def collect_energy_data(panel_id):
    #collecting energy data from the panel
    i2c_bus = board.I2C()
    sensor = adafruit_ina219.INA219(i2c_bus)
    sensor.gain = adafruit_ina219.GAIN_AUTO

    voltage = sensor.bus_voltage
    current = sensor.current
    power = voltage * current
    timestamp = time.time() #record timestamp of data collection

    # save energy data to database or file
    with open(f"panel_{panel_id}_energy_data.txt", "a") as f:
        f.write(f"{timestamp}, {voltage}, {current}, {power}\n")

    # calculate efficiency and energy production
    panel_area = 1.5  # assume panel area of 1.5 square meters
    irradiance = 1000  # assume solar irradiance of 1000 watts per square meter
    efficiency = power / (panel_area * irradiance) * 100  # calculate efficiency
    energy_production = power * 3600 / 1000  # calculate energy production in watt-hours per hour

    # save efficiency and energy production data to database or file
    with open(f"panel_{panel_id}_energy_stats.txt", "a") as f:
        f.write(f"{timestamp}, {efficiency:.2f}%, {energy_production:.2f} Wh/h\n")


# define the function to send an alert
def send_alert(source, message):
    #sending an alert message to the maintanence team
    # simulate sending an alert
    print(f"ALERT: {source}: {message}")

#A sun tracker typically uses sensors and motors to adjust the position of a solar panel to ensure that it is facing the sun at the optimal angle for maximum energy production.

def get_panel_azimuth_and_altitude(latitude, longitude):
    # get current date and time
    now = datetime.datetime.now()

    # calculate the day of year
    doy = now.timetuple().tm_yday

    # convert latitude and longitude to radians
    lat_rad = math.radians(latitude)
    long_rad = math.radians(longitude)

    # calculate the solar declination angle
    declination = -23.45 * math.cos(2 * math.pi / 365 * (doy + 10))

    # calculate the solar hour angle
    hour_angle = math.radians(15 * (now.hour - 12) + now.minute / 4 - longitude)

    # calculate the altitude angle
    altitude = math.asin(math.sin(lat_rad) * math.sin(declination) + math.cos(lat_rad) * math.cos(declination) * math.cos(hour_angle))

    # calculate the azimuth angle
    azimuth = math.atan2(-math.cos(declination) * math.sin(hour_angle), math.sin(altitude) * math.sin(lat_rad) - math.cos(altitude) * math.cos(lat_rad) * math.cos(hour_angle))
    azimuth = math.degrees(azimuth)
    if azimuth < 0:
        azimuth += 360

    # return the panel_azimuth and panel_altitude values
    panel_azimuth = azimuth
    panel_altitude = math.degrees(altitude)

    return panel_azimuth, panel_altitude

def get_sun_azimuth_and_altitude(latitude, longitude):
    # get current date and time
    now = datetime.datetime.now()

    # calculate the day of year
    doy = now.timetuple().tm_yday

    # convert latitude and longitude to radians
    lat_rad = math.radians(latitude)
    long_rad = math.radians(longitude)

    # calculate the solar declination angle
    declination = -23.45 * math.cos(2 * math.pi / 365 * (doy + 10))

    # calculate the solar hour angle
    hour_angle = math.radians(15 * (now.hour - 12) + now.minute / 4 - longitude)

    # calculate the altitude angle
    altitude = math.asin(math.sin(lat_rad) * math.sin(declination) + math.cos(lat_rad) * math.cos(declination) * math.cos(hour_angle))

    # calculate the azimuth angle
    azimuth = math.atan2(-math.cos(declination) * math.sin(hour_angle), math.sin(altitude) * math.sin(lat_rad) - math.cos(altitude) * math.cos(lat_rad) * math.cos(hour_angle))
    azimuth = math.degrees(azimuth)
    if azimuth < 0:
        azimuth += 360

    # return the sun_azimuth and sun_altitude values
    sun_azimuth = azimuth
    sun_altitude = math.degrees(altitude)

    return sun_azimuth, sun_altitude

def get_panel_angle(panel_id, latitude, longitude):
    # get the panel azimuth and altitude
    panel_azimuth, panel_altitude = get_panel_azimuth_and_altitude(latitude, longitude)

    # get the sun azimuth and altitude
    sun_azimuth, sun_altitude = get_sun_azimuth_and_altitude(latitude,longitude)
    # Calculate the angle between the sun and the panel
    angle = math.degrees(math.atan2(math.sin(sun_azimuth - panel_azimuth),
                                    math.cos(sun_altitude) * math.tan(panel_altitude) - math.sin(sun_altitude) * math.cos(sun_azimuth - panel_azimuth)))

    # Round the angle to two decimal places
    angle = round(angle, 2)

    return angle

# Function to adjust the angle of the solar panel based on the position of the sun
def adjust_panel_angle(panel_id,latitude,longitude):

    panel_angle = get_panel_angle(panel_id,latitude,longitude)

    # Determine the position of the panel based on the angle
    if panel_angle < -45:
        panel_position = "facing East"
    elif panel_angle >= -45 and panel_angle < 45:
        panel_position = "facing South"
    else:
        panel_position = "facing West"

    print(f"New Panel Angle is {panel_angle} , New panel position is {panel_position} ")
    print(f"Panel {panel_id} angle has been changed to {panel_angle} degrees")






# Initialize GPS
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

# Define panel locations
panel_locations = {
    "panel1": (10,20),
    "panel2": (30,40),
    "panel3": (50,60),
    "panel4": (70,80),
    "panel5": (90,100),
    "panel6": (110,120),
    "panel7": (130,140),
    "panel8": (150,160),
    "panel9": (170,180),
    "panel10": (190,200)
}

# Function to get panel ID based on GPS location
def get_panel_id(latitude, longitude):
    for panel_id, location in panel_locations.items():
        if location == (latitude, longitude):
            return panel_id
    return None

# Main

start_time = time.time()
while time.time() - start_time < 600:
    # Run the code here

        while True:
            try:
                report = session.next()
                # Check if we have a valid GPS fix
                if (report.mode == gps.MODE_2D or report.mode == gps.MODE_3D) and hasattr(report, "lat") and hasattr(report, "lon"):
                    # Get current latitude and longitude
                    latitude = report.lat
                    longitude = report.lon
                    # Get panel ID based on location
                    panel_id = get_panel_id(latitude, longitude)
                    panel_state = np.zeros(10,10)
                    if panel_id is not None:
                        # Do something with the panel ID
                        print(f"Panel {panel_id} is at latitude {latitude}, longitude {longitude}")
                        # Update panel state
                        panel_state[panel_id]["latitude"] = latitude
                        panel_state[panel_id]["longitude"] = longitude
                        # Monitor environment
                        monitor_environment(panel_id)
                        #adjusting the panel angle according to the sun position
                        adjust_panel_angle(panel_id,latitude,longitude)
                        #after determining the new panel angle , and new panel position , rotation of panel is taking place
                        panel_azimuth , panel_altitude = get_panel_azimuth_and_altitude(latitude , longitude)
                        #rotate_panels(panel_azimuth , panel_altitude )
                # Wait for some time before checking GPS again
                time.sleep(5)
            except Exception as e:
                print(e)
