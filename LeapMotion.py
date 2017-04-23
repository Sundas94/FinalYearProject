import sys, thread, time, math
import os, inspect

src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap

from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Motion Sensor Connected!"

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print "Motion Sensor Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()

        """ print "Frame ID: " + str(frame.id) \
            + "Timestamp: " + str(frame.timestamp) \
            + " # of Hands: " + str(len(frame.hands)) \
            + " # of Fingers: " + str(len(frame.fingers)) \
            + " # of Tools: " + str(len(frame.tools)) \
            + " # of Gestures: " + str(len(frame.gestures())) """

        # Getting hand data 
        """for hand in frame.hands:
            handType = "Left Hand" if hand.is_left else "Right Hand"

            print handType + " Hand ID: " + str(hand.id) + " Palm Position: " + str(hand.palm_position)

            normal = hand.palm_normal
            direction = hand.direction

            print "Pitch: " + str(direction.pitch * Leap.RAD_TO_DEG) + " Roll: " + str(normal.roll * Leap.RAD_TO_DEG)

            # Getting arm data
            arm = hand.arm
            print "Arm Direction: " + str(arm.direction) + " Wrist Position: " + str(arm.wrist_position) + " Elbow Postion: " + str(arm.elbow_position)
           
            # Getting finger data
            for finger in hand.fingers:
                print "Type: " + self.finger_names[finger.type] + " Finger ID: " + str(finger.id) + " Length(mm): " + str(finger.length) + " Width(mm): " + str(finger.width)

                # Bone data
                for b in range(0, 4): 
                    bone = finger.bone(b)
                    print "Bone: " + self.bone_names[bone.type] + " Start: " + str(bone.prev_joint) + " End: " + str(bone.next_joint) + " Direction: " + str(bone.direction)"""

            # Tools/Objects Data
        """for tools in frame.tools:
                print "Tool ID: " + str(tool.id) + " Tip position: " + str(tool.tip_position) + " Direction: " + str(tools.direction)"""

            # Gestures data
        for gesture in frame.gestures(): 
                """if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)

                    if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                        clockwiseness = "clockwise"
                    else:
                        clockwiseness= "anti-clockwise"

                    swept_angle = 0
                    if circle.state != Leap.Gesture.STATE_START:
                        previous = CircleGesture(controller.frame(1).gesture(circle.id))
                        swept_angle = (circle.progress - previous.progress) * 2 * Leap.PI

                    print "ID: " + str(circle.id) + " Progress: " + str(circle.progress) + " Radius(mm): " + str(circle.radius) \
                    + " Swept Angle: " + str(swept_angle * Leap.RAD_TO_DEG) + " " + clockwiseness"""
                

                # Recognising hand swiping gestures
                
                if gesture.type == Leap.Gesture.TYPE_SWIPE:
                    swipe = SwipeGesture(gesture)
                    """print "Swipe ID: " + str(swipe.id) + " State: " + self.state_names[gesture.state] + " Position: " + str(swipe.position) \
                    + " Direction: " + str(swipe.direction) + " Speed(mm/s): " + str(swipe.speed)"""
                    swipeDir = swipe.direction
                    if(swipeDir.x > 0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y)):
                        print "Swiped right"
                    elif(swipeDir.x < 0 and math.fabs(swipeDir.x) > math.fabs(swipeDir.y)):
                        print "Swiped left"
                    elif(swipeDir.y > 0 and math.fabs(swipeDir.x) < math.fabs(swipeDir.y)):
                        print "Swiped up"
                    elif(swipeDir.y < 0 and math.fabs(swipeDir.x) < math.fabs(swipeDir.y)):
                        print "Swiped down"



def main():
    listener = LeapMotionListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print "Press enter to quit"

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
