## Usage

Place images for red line removal and conversion to darknet format in raw_data file. Run red_removal.py. Access resulting files in out/data/images.

Add to <darknet.exe location>/cfg/ all files in accessory_files/cfg/ and add all remaining to darknet.exe location.

Run as "./darknet detector train cfg/obj.data cfg/yolo-obj.cfg darknet19_448.conv.23"