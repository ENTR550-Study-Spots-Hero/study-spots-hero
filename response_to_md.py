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
            case "busyness":
                spot[key] = int(response[i])
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


def general(spot):
    print(spot)
    queue = []
    if 1 < spot["comfortableTemp"] < 4:
        queue.append("- Really comforable.")
    if spot["busyness"] <= 1:
        queue.append("- Usually empty.")
    if True:
        queue.append(
            {
                0: "- No nearby restrooms.",
                1: "- No restrooms on the same floor.",
                2: "- No restrooms on the same floor.",
                3: "- Restrooms available on the same floor.",
                4: "- Restrooms are easy to find.",
                5: "- Restrooms within reach.",
            }[spot["restroomDistance"]]
        )
    print("".join(map(lambda x: x + "\n", queue)))
    return "".join(map(lambda x: x + "\n", queue))


def gen_md_file(spot, i):
    building_name = {
        "bbb": "Bob and Betty Beyster Building",
        "biomedical_engineering_building": "Biomedical Engineering Building",
        "chrysler": "Chrysler Center",
        "cooley_lab": "Cooley Lab",
        "dude": "Duderstadt Center",
        "fxb": "Francois-Xavier Bagnoud Building",
        "gg_brown": "G.G. Brown Laboratory",
        "naval_architecture_building": "Naval Architecture and Marine Engineering Building",
    }[spot["building"]]
    uniques = "".join(map(lambda x: f"- {x}\n", filter(lambda x: x != "", [
        spot["uniqueInfo"],
        spot["uniqueInfo2"],
        spot["uniqueInfo3"],
    ])))
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
title: "Study Spot {i} in {building_name}"
image: "{spot["image"]}"
---

Located: {spot["locationDetails"]}

#### Sketch
- {spot["furtherInfo"]}
{general(spot)}

{"#### Notes\n" if uniques != "" else ""}{uniques}
"""
    parent = "src/content/studySpotCollection"
    # parent = "./_study_spots"
    if not os.path.exists(f"{parent}"):
        raise Exception(f"Parent directory {parent} does not exist.")
    if not os.path.exists(f"{parent}/{spot['building']}"):
        os.makedirs(f"{parent}/{spot['building']}")
    with open(f"{parent}/{spot['building']}/{i}.md", "w+") as f:
        f.write(md)


def gen_md_files(study_spots):
    for building, spots in study_spots.items():
        for i, spot in enumerate(spots):
            gen_md_file(spot, i)


building_study_spots = responses_to_dict(sys.argv[1])
gen_md_files(building_study_spots)
