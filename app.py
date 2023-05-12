import os
from glob import glob
import json
import xml.dom.minidom as xml
from datetime import datetime as dt

local_path = os.path.dirname(os.path.realpath(__file__))

# Chemin des dossiers
data_folder = f"{local_path}/runtastic_export_data/"
sessions_folder = f"{data_folder}/Sport-sessions/"
cadence_folder = f"{sessions_folder}/Cadence-data/"
gps_folder = f"{sessions_folder}/GPS-data/"
hr_folder = f"{sessions_folder}/Heart-rate-data/"
speed_folder = f"{sessions_folder}/Speed-data/"
output_folder = f"{local_path}/output/"

# Types d'activités
runtastic_act_type = {"1": "Running", "3": "Biking", "4": "Biking", "19": "Other"}

for session_file in glob(f"{sessions_folder}*.json"):
	# Pour chaque session
	filename = os.path.basename(session_file)

	# On cherche les éventuells fichiers dans les sous-dossiers
	# Cadence
	cadence_file = glob(cadence_folder + filename)
	if cadence_file == []: cadence_file = None
	# GPS
	gps_file = glob(gps_folder + filename)
	if gps_file == []: gps_file = None
	# Heart rate
	hr_file = glob(hr_folder + filename)
	if hr_file == []: hr_file = None
	# Vitesse
	speed_file = glob(speed_folder + filename)
	if speed_file == []: speed_file = None

	# On lit le fichier de la session
	with open(session_file, "r") as file:
		session_data = json.loads(file.read())

	# Type de sport
	sport_id = None
	for feature in session_data["features"]:
		if feature["type"] != "initial_values":
			continue
		sport_id = feature["attributes"]["sport_type"]["id"]
		# start_time = dt.fromtimestamp(int(feature["attributes"]["start_time"])/1000)
		start_time = dt.strftime(dt.fromtimestamp(feature["attributes"]["start_time"]/1000), '%Y-%m-%dT%H:%M:%S.000Z')
	if sport_id is None:
		raise ValueError("Impossible de trouver le type de sport !")

	# On crée le xml
	xml_doc = xml.Document()
	xml_head = xml_doc.createElement("TrainingCenterDatabase")
	xml_head.setAttribute("xsi:schemaLocation", "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd")
	xml_head.setAttribute("xmlns:ns5", "http://www.garmin.com/xmlschemas/ActivityGoals/v1")
	xml_head.setAttribute("xmlns:ns3", "http://www.garmin.com/xmlschemas/ActivityExtension/v2")
	xml_head.setAttribute("xmlns:ns2", "http://www.garmin.com/xmlschemas/UserProfile/v2")
	xml_head.setAttribute("xmlns", "http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2")
	xml_head.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
	xml_head.setAttribute("xmlns:ns4", "http://www.garmin.com/xmlschemas/ProfileExtension/v1")
	xml_doc.appendChild(xml_head)

	xml_activities = xml_doc.createElement("Activities")
	xml_head.appendChild(xml_activities)

	xml_activity = xml_doc.createElement("Activity")

	xml_activity.setAttribute("Sport", runtastic_act_type[sport_id])
	xml_activities.appendChild(xml_activity)

	xml_element = xml_doc.createElement("Id")
	xml_element.appendChild(xml_doc.createTextNode(os.path.splitext(filename)[0]))
	xml_activity.appendChild(xml_element)

	xml_lap = xml_doc.createElement("Lap")
	xml_lap.setAttribute("StartTime", start_time)
	xml_activity.appendChild(xml_lap)


	



	with open(output_folder + os.path.splitext(filename)[0] + ".xml", "w") as output_file:
		output_file.write(xml_doc.toprettyxml(encoding="UTF-8").decode('UTF-8'))

	break