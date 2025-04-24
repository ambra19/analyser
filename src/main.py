#!/usr/bin/python3

import time
import signal
from loguru import logger
import roverlib
import roverlib.rovercom as rovercom
import logging
from datetime import datetime

# The main user space program
# this program has all you need from roverlib: service identity, reading, writing and configuration
def run(service : roverlib.Service, configuration : roverlib.ServiceConfiguration):
    #
    # Get configuration values
    #
    if configuration is None:
        raise ValueError("Configuration cannot be accessed")
    
    #
    # Access the to the identity of this service, who am I?
    #
    logger.info(f"Hello World, a new Python service {service.name} was born at version {service.version}")

    #
    # Reading from an input, to get data from other services (see service.yaml to understand the input name)
    #
    read_stream : roverlib.ReadStream = service.GetReadStream("energy", "energy")
    if read_stream is None:
        raise ValueError("Failed to get read stream")
    while True:
        data = read_stream.Read()
        if data is None:
            raise ValueError("Failed to read from 'energy' service")

        energy_data = data.energy_output
        if energy_data is None:
            return ValueError("Message does not contain energy output. What did energy do??")
            
        # ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # logger.info(f"Timestamp: [current time: {ct}] {energy_data}")
        # time = datetime.fromtimestamp(data.timestamp / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"[{data.timestamp}]{energy_data}")
        # ts_readable = datetime.fromtimestamp(data.timestamp / 1000.0).strftime("%Y-%m-%d %H:%M:%S")

        # logger.info(
        #     f"[{ts_readable}] "
        #     f"V: {energy_data.supply_voltage:.2f} V | "
        #     f"I: {energy_data.current_amps:.3f} A | "
        #     f"P: {energy_data.power_watts:.2f} W"
        # )

    
    
    # WRITING TO AN OUTPUT STREAM -- NOT USED FOR NOW -- Check the template for the example

    # Writing to an output that other services can read (see service.yaml to understand the output name)
    #
    # write_stream : roverlib.WriteStream = service.GetWriteStream("decision")
    # if write_stream is None:
    #     raise ValueError("Failed to create write stream 'decision'")

    # while True:
    #     #
    #     # Reading one message from the stream
    #     #
    #     data = read_stream.Read()
    #     if data is None:
    #         raise ValueError("Failed to read from 'energy' service")
        
    #     # When did the imaging service create this message
    #     created_at = data.timestamp
    #     logger.info(f"Received message with timestamp: {created_at}")

        # Get the imaging data
        # imaging_data = data.camera_output
        # if imaging_data is None:
        #     return ValueError("Message does not contain camera output. What did imaging do??")

        # logger.info(f"Imaging service captured a {imaging_data.trajectory.width} by {imaging_data.trajectory.height} image"
        


# This function gets called when the pipeline gets terminated. This can happen if any other service
# in the pipeline crashes or if the pipeline is stopped via the the web interface.
def on_terminate(sig : signal):
    logger.info(f"signal: {str(sig)}, Terminating service")

    #
    # ...
    # If you need to add clean up logic, add it here
    # ...
    #

    return None

if __name__ == "__main__":
    roverlib.Run(run, on_terminate)
