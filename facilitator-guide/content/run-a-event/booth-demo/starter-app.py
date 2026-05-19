from flask import Flask, render_template, jsonify, send_from_directory
from jinja2.exceptions import TemplateNotFound
import requests
import time
import threading
import os
import config
import math
from lib.robot_utils import (
    log_with_timestamp,
    bypass_obstacle,
    search_for_hat_step,
    get_stream_data,
    move_forward,
    turn_left,
    turn_right,
    move_backward,
    distance,
    distance_int,
    take_picture_and_detect_objects,
    find_highest_score,
    take_picture
)

# Defined variables for Flask proxy/web/application server
application = Flask(__name__)
application.config.from_object('config')
thread_event = threading.Event()

# Defined model parameters
image_resolution_x = 640
delta_threshold = 280
hat_found_and_intercepted = False
min_distance_to_obstacle = 300
angle_delta = 90

def search_for_hat():
    # Define switch for identifying found and intercepted hats across functions
    global hat_found_and_intercepted

    print('\n### Search For Hat Mode - START ###')

    # Circle, capture images, apply model and drive towards an identified object
    turn_counter = 0
    while thread_event.is_set():
        print('\n')

        # Take picture and find the object with the highest probabilty of being a hat
        objects = take_picture_and_detect_objects()
        coordinates = find_highest_score(objects)

        # Output distance from sensor
        print ('Got distance -> ', distance())


        # Align to and drive towards identified object
        if coordinates and coordinates.confidence_score > config.CONFIDENCE_THRESHOLD:
            print(f'''Object with highest score -> [
                confidence score: {coordinates.confidence_score},
                x upper left corner: {coordinates.x_upper_left},
                y upper left corner: {coordinates.y_upper_left},
                x lower right corner: {coordinates.x_lower_right},
                y lower right corner: {coordinates.y_lower_right},
                object class: {coordinates.object_class} ]''')

            # Align so that the most likely hat identified is in the center (within 20 pixels)
            center_x = (coordinates.x_upper_left + coordinates.x_lower_right) / 2
            print(f'center_x: {center_x}')

            # Center of hat needs to be within 20 pixels
            if abs(image_resolution_x/2-center_x) >= 20:
                if center_x < 320:
                    turn_left(10)
                else:
                    turn_right(10)

            # Determine size of the object in the image (not the real size!)
            delta = coordinates.x_lower_right - coordinates.x_upper_left
            print(f'delta: {delta}')

            hat_found_and_intercepted = True

            # Happy Dance, would be better to have a loop for this
            move_forward(5)
            move_backward(5)
            move_forward(5)
            move_backward(5)
            move_forward(5)
            move_backward(5)

            print('### Search For Hat Mode - END: OJECT FOUND ! ###')
            return

        else:
            # Circle in case no hat could be identied
            if turn_counter <= 360:
                turn_right(10)
                turn_counter = turn_counter + 10
            else:
                # After a full circle, move forward and circle again to find the hat
                #move_forward(40)
                print('turn complete, resetting!')
                turn_counter = 0

    print('### Search For Hat Mode - END ###')

# Check for an obstacle directly in front and bypass it, if existing
def bypass_obstacle():
    # Determine if an obstacle is in sight
    obstacle_in_sight = distance_int() <= min_distance_to_obstacle

    # Only continue if an obstacle is ahead
    if not obstacle_in_sight:
        print ('No obstacle close enough -> returning')
        return

    # For debugging only
    take_picture('static/current_view.jpg')

    # Determine distance to obstacle
    distance_to_object = distance_int()

    print('### Bypass Obstacle Mode - START ###')

    # Turn left
    turn_left(angle_delta)

    # Determine if there is another obstacle is in sight
    obstacle_in_sight = distance_int() <= min_distance_to_obstacle
    print ('Got distance -> ', distance())

    # If no other obstacle is in the bypass direction, move a bit forward
    # and then go back again on course
    if not obstacle_in_sight:
        move_forward(20)
        turn_right(angle_delta)

    # Determine if original obsctacle is still in sight (after having turned back in original direction)
    obstacle_in_sight = distance_int() <= min_distance_to_obstacle
    print ('Got distance -> ', distance())

    # If original obstacle is not in sight anymore, move forward to bypass it
    if not obstacle_in_sight:
        # Move forward using the original distance to the obstacle and a buffer
        move_forward(math.ceil(distance_to_object / 10) + 40)

    print('### Bypass Obstacle Mode - END: SUCCESS! ###')

# Function you will be working on
def startRobot():

    # Drop your code here

    ## Movement Code
    # move_forward(10)
    # turn_left(90)
    # turn_right(180)
    # turn_left(90)
    # move_backward(10)

    ## Distance Test
    # dist = distance()
    #print ('Got distance -> ', dist)

    ## Object Detection Code
    # objects = take_picture_and_detect_objects()
    # coordinates = find_highest_score(objects)

    #if coordinates:
    #    print(f'''Object with highest score -> [
    #        confidence score: {coordinates.confidence_score},
    #        x upper left corner: {coordinates.x_upper_left},
    #        y upper left corner: {coordinates.y_upper_left},
    #        x lower right corner: {coordinates.x_lower_right},
    #        y lower right corner: {coordinates.y_lower_right},
    #        object class: {coordinates.object_class} ]''')
    #else:
    #    print('No objects found')

    ## Self Developed Code
    #while thread_event.is_set():
    #    log_with_timestamp("Entering main control loop.")
    #
    #    # Put your checks and movement commands here
    #    while int(distance()) > 15:
    #        objects = take_picture_and_detect_objects()
    #        coordinates = find_highest_score(objects)#

    #        if coordinates:
    #            print(f'''Object with highest score -> [
    #                confidence score: {coordinates.confidence_score},
    #                x upper left corner: {coordinates.x_upper_left},
    #                y upper left corner: {coordinates.y_upper_left},
    #                x lower right corner: {coordinates.x_lower_right},
    #                y lower right corner: {coordinates.y_lower_right},
    #                object class: {coordinates.object_class} ]''')
    #
    #            move_forward(int(distance())-5)
    #            break
    #
    #        turn_right(20)
    #    print('Done')

    #log_with_timestamp("Exited main control loop.")
    #print('Done')

    # Control App
    global hat_found_and_intercepted
    hat_found_and_intercepted = False
    log_with_timestamp("startRobot thread has started.")

    while thread_event.is_set() and not hat_found_and_intercepted:

        # bypass_obstacle()

        search_for_hat()

    log_with_timestamp("Exited main control loop.")

# API and helper functions
@application.route('/')
def index():
    return render_template('index.html')

@application.route('/run', methods=['POST'])
def run():
    try:
        log_with_timestamp("/run endpoint called.")
        thread_event.set()
        log_with_timestamp("Creating and starting the startRobot thread.")
        thread = threading.Thread(target=startRobot)
        thread.start()
        log_with_timestamp("/run endpoint finished and returned 'Robot started'.")
        return "Robot started"
    except Exception as error:
        return str(error)

@application.route('/stop', methods=['POST'])
def stop():
    try:
        log_with_timestamp("/stop endpoint called.")
        thread_event.clear()
        return "Robot stopped"
    except Exception as error:
        return str(error)

@application.route('/status', methods=['POST'])
def status():
    response = requests.get(application.config['ROBOT_API'] + '/remote_status?user_key=' + application.config['ROBOT_NAME'], verify=False)
    return response.text

@application.route('/get_stream', methods=['GET'])
def stream():
    """
    Web route to get the plain camera image stream.
    Calls the utility function to handle the logic.
    """
    data, status_code = get_stream_data()
    return jsonify(data), status_code

@application.route('/<string:page_name>')
def serve_page(page_name):
    try:
        return render_template(f'{page_name}.html')
    except TemplateNotFound:
        return "<h1>Page not found</h1><p>The requested page does not exist.</p>", 404

@application.route('/templates/<path:filename>')
def serve_template_asset(filename):
    return send_from_directory(os.path.join(application.root_path, 'templates'), filename)

if __name__ == '__main__':
   application.run(host="0.0.0.0", port=8080)
