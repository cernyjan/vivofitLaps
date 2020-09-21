import sys
import xml.etree.ElementTree as ET
import datetime
from datetime import datetime


def into_float(value):
    try:
        return float(value)
    except ValueError:
        sys.exit("Unexpected input format, existing...")

def into_int(value):
    try:
        return int(value)
    except ValueError:
        sys.exit("Unexpected input format, existing...")


class Activity:
# ./Activities/Activity/Id,Lap/TotalTimeSeconds,DistanceMeters/Track/Trackpoint[]/Time,DistanceMeters
# TrainingCenterDatabase (real root)
# Activities (= ~root)
# Activity Sport="Running"
# Activity - Id (= <Lap StartTime="")
# Activity - Lap - TotalTimeSeconds, DistanceMeters
# Activity - Lap - Track - Trackpoint ([]) - Time, DistanceMeters
# Activity - Lap - Creator - Name
# Activity - Lap - Creator - Version ( - VersionMajor, VersionMinor, BuildMajor, BuildMinor)

    def __init__(self, activity_type='Running'):
        self.id = ''
        self.activity_type = activity_type
        self.total_time_seconds = 0
        self.total_distance_meters = 0
        self.device_name = ''
        self.device_version = ''

    def get_total_laps(self):
        return int(self.total_distance_meters // 1000)


if __name__ == '__main__':
    file_path = ""
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("tcx file path: ")

    tree = ET.parse(file_path)
    root = tree.getroot()

    activity = Activity(root[0][0].attrib['Sport'])
    activity.id = root[0][0][0].text
    activity.device_name = root[0][0][2][0].text
    activity.device_version = "{}.{}.{}.{}".format(root[0][0][2][3][0].text, root[0][0][2][3][1].text, root[0][0][2][3][2].text,root[0][0][2][3][3].text)
    activity.total_time_seconds = into_float(root[0][0][1][0].text)
    activity.total_distance_meters = into_float(root[0][0][1][1].text)
    
    print(activity.id)
    print(activity.device_name)
    print(activity.device_version)
    print(activity.total_time_seconds)   
    print(activity.total_distance_meters)
    print(activity.get_total_laps())

    track = root[0][0][1][6]
    start_datetime = datetime(into_int(activity.id.split('T')[0].split('-')[0]), 1, 1)
    print(start_datetime)
    distancemeters = 0.0
    for lap in range(activity.get_total_laps()):
        for trackpoint in track:
            distancemeters = into_float(trackpoint[1].text)
            if distancemeters // 1000 >= (lap + 1):
                print(trackpoint[0].text)
                print(trackpoint[1].text)
                break

    
    