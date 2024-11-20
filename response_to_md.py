import csv
import sys
import os

keys = [
    "timestamp",
    "image",
    "building",
    "locationDetails",
    # note these two are combined into one field
    "isQuiet",
    "isCollaborative",
    # 0-5 scale, diff meanings
    "caenAccess",
    "naturalLight",
    "comfortableTemp",
    "outletAvailability",
    "furnitureComfort",
    "restroomDistance",
    "reservable",
    "busyness",
    # text
    "furtherInfo",
    "uniqueInfo",
    "uniqueInfo2",
    "uniqueInfo3",
]


def row_to_spot(response: list) -> dict:
    spot = {}
    i = 0
    for __, key in enumerate(keys):
        # timestamp, image, building, locationDetails go smoothly
        match key:
            case "isQuiet":
                spot[key] = "Quiet" in response[i]
                i -= 1
            case "isCollaborative":
                spot[key] = "Collaborative" in response[i]
            case "caenAccess":
                print(response)
                print(i)
                spot[key] = int(response[i]) > 0
            case "naturalLight":
                spot[key] = int(response[i])
            case "comfortableTemp":
                spot[key] = int(response[i])
            case "outletAvailability":
                spot[key] = int(response[i])
            case "furnitureComfort":
                spot[key] = int(response[i])
            case "restroomDistance":
                spot[key] = int(response[i])
            case "reservable":
                spot[key] = int(response[i]) > 0
            case "building":
                spot[key] = str(response[i]).lower().replace(" ", "_")
            case _:
                spot[key] = response[i]
        i += 1
    return spot


def responses_to_dict(response_file):
    study_spots = {}
    with open(response_file, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        print(header)
        for row in reader:
            spot = row_to_spot(row)
            building = spot["building"]
            if building not in study_spots:
                study_spots[building] = []
            study_spots[building].append(spot)
    return study_spots


def gen_md_file(spot, i):
    md = f"""---
building: "{spot["building"]}"
timestamp: "{spot["timestamp"]}"
isQuiet: {spot["isQuiet"]}
isCollaborative: {spot["isCollaborative"]}
caenAccess: {spot["caenAccess"]}
naturalLight: {spot["naturalLight"]}
comfortableTemp: {spot["comfortableTemp"]}
outletAvailability: {spot["outletAvailability"]}
furnitureComfort: {spot["furnitureComfort"]}
restroomDistance: {spot["restroomDistance"]}
reservable: {spot["reservable"]}
busyness: {spot["busyness"]}
title: "Study Spot {i} in {spot["building"]}"
---

# Study Spot {i} in {spot["building"]}

location details: {spot["locationDetails"]}

{spot["furtherInfo"]}

{spot["uniqueInfo"]}

{spot["uniqueInfo2"]}

{spot["uniqueInfo3"]}
"""
    if not os.path.exists(f"./_study_spots/{spot['building']}"):
        os.makedirs(f"./_study_spots/{spot['building']}")
    with open(f"./_study_spots/{spot['building']}/{i}.md", "w+") as f:
        f.write(md)


def gen_md_files(study_spots):
    for building, spots in study_spots.items():
        for i, spot in enumerate(spots):
            gen_md_file(spot, i)


building_study_spots = responses_to_dict(sys.argv[1])
gen_md_files(building_study_spots)
