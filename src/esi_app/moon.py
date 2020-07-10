from datetime import datetime, timedelta
from json import dump, load


def CalcDistance(bm_1, bm_2):
    # Works for two bookmarks
    try:
        # Rounds to 3 decimal places
        rounded = lambda num : round(num, 3)
        # Gets single coordinate
        xyz_coordinate = lambda coordinates, xyz : coordinates[xyz]
        # Gets all coordinates, passes to xyz_coordinate to get single coordinate
        coordinate = lambda bm, xyz : xyz_coordinate(bm['coordinates'], xyz)
        # Partial calc from distance formula
        calc = lambda bm_1, bm_2, xyz : (coordinate(bm_1, xyz) - coordinate(bm_2, xyz)) ** 2
        # Distance formula
        distance = (calc(bm_1, bm_2, 'x') + calc(bm_1, bm_2, 'y') + calc(bm_1, bm_2, 'z')) ** 0.5

    # Works for one bookmark and a structure
    except:
        # Rounds to 3 decimal places
        rounded = lambda num : round(num, 3)
        # Gets single coordinate
        xyz_coordinate = lambda coordinates, xyz : coordinates[xyz]
        # Gets all coordinates/position, passes to xyz_coordinate to get single coordinate
        coordinate = lambda bm, xyz : xyz_coordinate(bm['coordinates'], xyz)
        position = lambda bm, xyz : xyz_coordinate(bm['position'], xyz)
        # Partial calc from distance formula
        calc = lambda bm_1, bm_2, xyz : (coordinate(bm_1, xyz) - position(bm_2, xyz)) ** 2
        # Distance formula
        distance = (calc(bm_1, bm_2, 'x') + calc(bm_1, bm_2, 'y') + calc(bm_1, bm_2, 'z')) ** 0.5

    return rounded(distance)


def CalcDuration(bm_1, bm_2):
    # Converts unicode time to datetime object
    created = lambda bm : bm['created']

    # Calculates difference between times, in seconds
    time_string_1 = str(created(bm_1)).split('+')[0]
    time_string_2 = str(created(bm_2)).split('+')[0]
    duration = (
        datetime.strptime(time_string_1,'%Y-%m-%dT%H:%M:%S') -
        datetime.strptime(time_string_2,'%Y-%m-%dT%H:%M:%S')
    )

    return abs(duration.total_seconds())


def CalcSpeed(distance, duration):
    # Rounds to 3 decimal places
    rounded = lambda num : round(num, 3)

    # Speed in m/s
    try:
        speed = rounded(distance) / rounded(duration)
    except:
        speed = 0

    # Binning speeds
    # if speed < 0.4 and speed > 0.1:
    #     binned_speed = 0.25
    # if speed < 0.6 and speed > 0.4:
    #     binned_speed = 0.525
    # if speed < 0.9 and speed > 0.6:
    #     binned_speed = 0.75
    # if speed < 1.2 and speed > 0.9:
    #     binned_speed = 1

    return rounded(speed)


def CalcEta(distance, speed, bm_2):
    # Converts unicode time to datetime object
    created = lambda bm : bm['created']

    # Rounds to 3 decimal places
    rounded = lambda num : round(num, 3)

    # Speed in m/s
    try:
        duration = rounded(distance) / rounded(speed)
    except:
        duration = 0
    time_string = str(created(bm_2)).split('+')[0]
    eta = datetime.strptime(time_string,'%Y-%m-%dT%H:%M:%S') + timedelta(seconds=duration)

    return eta


def moon(character, moon_times):
    bookmark_data = character.bookmarks()

    for bookmark in bookmark_data:
        chunk_1 = bookmark

        # Loop through list backwards to find matching bookmark
        for bookmark in bookmark_data[::-1]:

            # If we make it back to bookmark 1
            if bookmark == chunk_1:
                break

            # If a matching bookmark is found
            if bookmark['label'] == chunk_1['label'] and bookmark['location_id'] == chunk_1['location_id']:
                chunk_2 = bookmark
                structure_name = str(chunk_1['label']).split('\t')[0].split('(')[0]
                chunk_movement_distance = CalcDistance(chunk_1, chunk_2)
                chunk_movement_duration = CalcDuration(chunk_1, chunk_2)
                chunk_speed = CalcSpeed(chunk_movement_distance, chunk_movement_duration)

                try:
                    structure = character.structure_search(structure_name)
                    structure_id = structure['structure']
                    athanor = character.structure_info(structure_id)
                    athanor_distance = CalcDistance(chunk_2, athanor) - 165000
                    chunk_eta = CalcEta(athanor_distance, chunk_speed, chunk_2)
                    moon_times[structure_name] = {
                        "chunk_eta": chunk_eta
                    }
                except:
                    moon_times[structure_name] = 'Structure not found'
                break

    return moon_times

if __name__== "__main__":
    main()
