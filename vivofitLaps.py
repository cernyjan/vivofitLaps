import sys
import xml.etree.ElementTree as ET


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
        self.activity_type = activity_type
        self.total_time_seconds = 0
        self.total_distance_meters = 0
        self.total_laps = 0

    def get_total_time_seconds(self):
        return self.total_time_seconds

    def get_total_distance_meters(self):
        return self.total_time_seconds

if __name__ == '__main__':
    file_path = ""
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("tcx file path: ")

    tree = ET.parse(file_path)
    root = tree.getroot()
    
    for child in root:
        print(child.tag)
        print(child.attrib)

    print(root[0][0][0].text)

    print(root[0][0][1][0].text)
    print(root[0][0][1][1].text)
        


    