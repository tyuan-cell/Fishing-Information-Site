from dataclasses import dataclass

@dataclass
class Season:
    first_month: str
    first_day: str
    last_month: str
    last_day: str

@dataclass
class Fish:
    common_names: list[str]
    min_size: float
    max_size: float
    season: list[Season]

all_fish_list = [
    Fish(["Striped Bass", "Rockfish"], 28.0, 31.0, [Season("January", "1", "December", "31")]),
Fish(["Summer Flounder", "Fluke"], 17.5, 999.9, [Season("June", "1", "December", "31")]),
Fish(["Black Sea Bass"], 12.5, 999.9, [Season("May", "1", "December", "31")]),
Fish(["Weakfish", "Gray Trout", "Sea Trout"], 13.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Bluefish"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Tautog", "Blackfish"], 16.0, 999.9, [Season("January", "1", "May", "15"), Season("July", "1", "December", "31")]),
Fish(["Scup", "Porgy"], 9.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Red Drum", "Channel Bass"], 20.0, 27.0, [Season("January", "1", "December", "31")]),
Fish(["Black Drum"], 16.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Atlantic Croaker"], 8.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Kingfish", "Whiting"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Spanish Mackerel"], 14.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["King Mackerel"], 23.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Cobia"], 43.0, 999.9, [Season("June", "15", "September", "15")]),
Fish(["Spotted Seatrout"], 12.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Sheepshead"], 14.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Triggerfish", "Gray Triggerfish"], 12.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Mahi Mahi", "Dolphin Fish", "Dorado"], 20.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Yellowfin Tuna"], 27.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Bluefin Tuna"], 27.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Bigeye Tuna"], 27.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Wahoo"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["White Marlin"], 66.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Blue Marlin"], 99.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Swordfish"], 47.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Shortfin Mako Shark"], -999.9, 0.0, [Season("January", "1", "December", "31")]),
Fish(["Sand Tiger Shark"], -999.9, 0.0, [Season("January", "1", "December", "31")]),
Fish(["Thresher Shark"], 54.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Smooth Dogfish", "Smoothhound Shark"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Spiny Dogfish"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Largemouth Bass"], 12.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Northern Snakehead"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Channel Catfish"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Blue Catfish"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Flathead Catfish"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["White Catfish"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Brown Bullhead"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Chain Pickerel"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Northern Pike"], 24.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Black Crappie"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["White Crappie"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Bluegill"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Redear Sunfish", "Shellcracker"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Pumpkinseed Sunfish"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Yellow Perch"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["White Perch"], 0.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Walleye"], 15.0, 999.9, [Season("January", "1", "December", "31")]),
Fish(["Rainbow Trout"], 0.0, 999.9, [Season("March", "1", "February", "28")]),
Fish(["Brown Trout"], 0.0, 999.9, [Season("March", "1", "February", "28")])
                 ]
