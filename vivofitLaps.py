import sys
import xml.etree.ElementTree as ET
import datetime
from datetime import datetime


def into_float(value):
    try:
        return float(value)
    except ValueError:
        sys.exit("Unexpected input format, exiting...")

def into_int(value):
    try:
        return int(value)
    except ValueError:
        sys.exit("Unexpected input format, exiting...")

def get_date_format(value):
    date = value.split('T')[0].split('-')
    time = value.split('T')[1].split('Z')[0].split(':')
    head, sep, tail = time[2].partition('.')
    time[2] = head
    return datetime(into_int(date[0]), into_int(date[1]), into_int(date[2]), into_int(time[0]), into_int(time[1]), into_int(time[2]))


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
        self.total_completed_laps = 0
        self.track = None
        self.device_name = ''
        self.device_version = ''

    def set_total_laps(self):
        self.total_completed_laps = int(self.total_distance_meters // 1000)

    def render_info(self):
        print(self.id)
        print(self.device_name)
        print(self.device_version)
        print(self.total_time_seconds)   
        print(self.total_distance_meters)
        print(self.total_completed_laps)

    def get_lap(self, index, start_datetime, finish_datetime):
        print("{}.".format(index))
        print(finish_datetime - start_datetime)

    def render_laps(self):
        if self.total_distance_meters < 1000:
            print('1.')
            print(self.total_distance_meters)
            print(self.total_time_seconds)
        else:
            if self.track == None:
                sys.exit("No valid input data (missing track in tcx file), exiting...")
            else:
                lap_number = 1
                start_datetime = get_date_format(activity.id)
                distance_meters = 0.0
                track_number = 1
                track_count = len(self.track)
                for trackpoint in self.track:
                    distance_meters = into_float(trackpoint[1].text)
                    if distance_meters // 1000 >= lap_number:
                        #print(start_datetime)
                        finish_datetime = get_date_format(trackpoint[0].text)
                        #print(finish_datetime)
                        #print(trackpoint[0].text)
                        #print(trackpoint[1].text)
                        self.get_lap(lap_number, start_datetime, finish_datetime)
                        start_datetime = finish_datetime
                        lap_number = lap_number + 1
                    elif track_number == track_count:
                        finish_datetime = get_date_format(trackpoint[0].text)
                        self.get_lap(lap_number, start_datetime, finish_datetime)
                        print(trackpoint[1].text)
                    track_number = track_number + 1
    
    
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
    activity.set_total_laps()
    activity.track = root[0][0][1][6]
    
    activity.render_info()
    activity.render_laps()