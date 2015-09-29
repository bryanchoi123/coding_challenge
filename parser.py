from mapper import mappings
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime

LOG_FILE = "./MRSI_VISION.LOG"
MAP_FILE = "./filename-mappings.csv"

# get filename mappings
fileMappings = mappings(MAP_FILE)

# map filename -> [(timestamp, score)] array of tuples
scoreMappings = {}
for key in fileMappings.keys():
    scoreMappings[key] = []

# open log file
logFile = open(LOG_FILE, "r")

lensFileName = ""
fiducialFound = False
minTime = datetime.datetime.strptime("18:07:05:422", "%H:%M:%S:%f")
maxTime = datetime.datetime.strptime("16:29:04:188", "%H:%M:%S:%f")
minScore = 100.0
maxScore = 0.0
for line in logFile:
    # parse out timestamp from rest of line
    timeStampString = line[:12]

    # sometimes in the format of H:M: S:MS or H:M:S: MS instead of H:M:S:MS
    timeSplit = timeStampString.split(" ")
    timeStampString = timeSplit[0]
    for i in range(len(timeSplit)-1):
        timeStampString += "0" + timeSplit[i+1]
    
    timeStamp = datetime.datetime.strptime(timeStampString, "%H:%M:%S:%f")
    infoLine = line[13:]

    # line that contains file name
    if infoLine.startswith("Loading VisionData from file"):
        fileSplit = infoLine.split("\\")
        # break off new line character at the end
        fileName = fileSplit[-1][:-1]
        if fileName in fileMappings:
            lensFileName = fileName
    # fiducial found indicates incoming score
    elif infoLine.startswith("Fiducial was found"):
        fiducialFound = True
    # grab score and save it with timestamp
    elif fiducialFound and infoLine.startswith("Map"):
        fiducialFound = False
        scoreSplit = infoLine.split(", ")
        score = scoreSplit[-2]

        scoreValueSplit = score.split(": ")
        scoreValue = float(scoreValueSplit[1])
        scoreMappings[lensFileName].append((timeStamp, scoreValue))

        # do comparisons for maxes/mins
        if timeStamp < minTime:
            minTime = timeStamp
        if timeStamp > maxTime:
            maxTime = timeStamp
        if scoreValue < minScore:
            minScore = scoreValue
        if scoreValue > maxScore:
            maxScore = scoreValue

logFile.close()

# set up plot titles
plt.xlabel("Timestamp")
plt.ylabel("Score")

# set up plot x-axis
axesFormat = md.DateFormatter("%H:%M:%S")
axes = plt.gca()
axes.xaxis.set_major_formatter(axesFormat)

# set up y-axis
plt.ylim(65, 100)

for lens in sorted(scoreMappings.keys()):
    scores = []
    times = []
    for timeTuple in scoreMappings[lens]:
        times.append(timeTuple[0])
        scores.append(timeTuple[1])
    # change dates to numbers to use for x-axis
    dates = md.date2num(times)
    plt.plot(dates, scores, "o-", label=fileMappings[lens])
    plt.legend(loc="lower left", fontsize="medium")
plt.grid()
plt.show()
