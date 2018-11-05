import json, shlex, subprocess
import sys
from openalpr import Alpr

class PlateReader:



    def __init__(self, picname):
        #webcam subprocess args
        webcam_command = "fswebcam -r 640x480 -S 20 --no-banner --quiet alpr.jpg"
        self.webcam_command_args = shlex.split(webcam_command)

        # alpr subprocess args
        alpr_command = "alpr -c eu -t hr -n 300 -j " + picname
        # alpr_command = "alpr -c au -p nsw -n 10 -j alpr.jpg"
        self.alpr_command_args = shlex.split(alpr_command)

        self.alpr = Alpr("us", "/Users/lukelian/PycharmProjects/plate_recognition_CZTech/openalpr.conf",
                    "/Users/lukelian/PycharmProjects/plate_recognition_CZTech/runtime_data")
        if not self.alpr.is_loaded():
            print("Error loading OpenALPR")
            sys.exit(1)
        else:
            print("Correct loading OpenALPR")



    def webcam_subprocess(self):
        return subprocess.Popen(self.webcam_command_args, stdout=subprocess.PIPE)

    def alpr_subprocess(self):
        return subprocess.Popen(self.alpr_command_args, stdout=subprocess.PIPE)


    def alpr_json_results(self):
        self.webcam_subprocess().communicate()
        alpr_out, alpr_error = self.alpr_subprocess().communicate()

        if not alpr_error is None:
            return None, alpr_error
        elif b"No license plates found." in alpr_out:
            return None, None

        try:
            return json.loads(alpr_out.decode("utf-8")), None
        except ValueError as e:
            return None, e


    def read_plate(self):
        alpr_json, alpr_error = self.alpr_json_results()

        if not alpr_error is None:
            print(alpr_error)
            return

        if alpr_json is None:
            print("No results!")
            return

        results = alpr_json["results"]

        ordinal = 0
        for result in results:
            candidates = result["candidates"]

            for candidate in candidates:
                ordinal += 1
                prefix = "-"
                if candidate['matches_template']:
                    prefix = "*"
                with open("jieguo.txt", "w") as f:
                    f.write("Guess {0:d}: {1:s} {2:.2f}%".format(ordinal, candidate["plate"], candidate["confidence"]))
                print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
                # print ("Guess {0:d}: {1:s} {2:.2f}%".format(ordinal, candidate["plate"], candidate["confidence"]))

    def read_plate_py(self, picname):
        # self.webcam_subprocess().communicate()
        self.alpr.set_top_n(20)
        self.alpr.set_default_region("md")
        results = self.alpr.recognize_file(picname)
        i = 0
        for plate in results['results']:
            i += 1
            print("Plate #%d" % i)
            print("   %12s %12s" % ("Plate", "Confidence"))
            for candidate in plate['candidates']:
                prefix = "-"
                if candidate['matches_template']:
                    prefix = "*"
                print("  %s %12s%12f" % (prefix, candidate['plate'], candidate['confidence']))
                break

    def unload(self):
        self.alpr.unload()

if __name__=="__main__":
    plate_reader = PlateReader("alpr.jpg")
    plate_reader.read_plate_py(picname="alpr.jpg")
    # Call when completely done to release memory
    plate_reader.unload()
