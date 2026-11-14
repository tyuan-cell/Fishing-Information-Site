from dataclasses import dataclass
from bakery import assert_equal
from drafter import *
from Fish import all_fish_list, Fish, Season
from fish_images import fish1, fish_image_list

set_website_title("Delaware Fishing Regulations")
set_site_information(
    author="Thomas Yuan",
    description="Find regulation information for fish in Delaware waters.",
    sources="Thanks to the Drafter docs and the RISE cohort.",
    planning=[""],
    links=["https://github.com/your-username/your-repository"]
)
hide_debug_information()
set_website_framed(False)

NO_FISH = Fish(["Unknown Fish"], 0.0, 0.0, [])

@dataclass
class State:
    fish_search: str
    matching_fish: list[Fish]
    selected_fish: Fish
    current_page: str

@route
def fish_search_result(state: State, name_searched: str) -> Page:
    """Consumes the current application state and a search string,
    filtering all_fish_list for matching fish names and routing to the appropriate page.

    Args:
        state (State): the current state of the application.
        name_searched (str): the fish name or partial name entered by the user.

    Returns:
        Page: the fish_information page if one match is found, choose_from_list if multiple
              matches are found, or index if no matches are found."""
    state.fish_search = name_searched #change to search = state.fish_search
    state.matching_fish = []
    for fish in all_fish_list:
        for name in fish.common_names:
            if name_searched.lower() in name.lower():
                state.matching_fish.append(fish)
                break
    if len(state.matching_fish) > 1:
        state.selected_fish = NO_FISH
        return choose_from_list(state)
    elif len(state.matching_fish) == 1:
        state.selected_fish = state.matching_fish[0]
        return fish_information(state)
    elif len(state.matching_fish) == 0:
        return index(state)

@route
def choose_from_list(state: State) -> Page:
    """Consumes the current application state containing multiple matching fish,
    producing a selection page displaying each candidate's image, name, and an input box.

    Args:
        state (State): the current state containing matching_fish options.

    Returns:
        Page: a Drafter Page listing matching fish options and selection controls."""
    content = [Header("Please Identify the Correct "),
               Text("Type in the Correct  Below:")]
    for fish in state.matching_fish:
        for fish1_object in fish_image_list:
            if fish1_object.name == fish.common_names[0]:
                grouped_pics = Div(Text(fish.common_names[0]), LineBreak(),
                                   Image(fish1_object.url))
                content.append(grouped_pics)
                break
    content.append(TextBox("chosen_name", ""))
    content.append(Button("Select ", select_chosen_fish))
    content.append(Button("Return Home", go_home))
    return Page(state, content)

@route
def select_chosen_fish(state: State, chosen_name: str) -> Page:
    """Consumes the current application state and the user's typed fish name,
    updating selected_fish and routing to its details page if valid.

    Args:
        state (State): the current state of the application.
        chosen_name (str): the exact primary fish name entered by the user.

    Returns:
        Page: the fish_information page if chosen_name matches a candidate, or
              choose_from_list again if no match is found."""
    for fish in state.matching_fish:
        if chosen_name.lower() == fish.common_names[0].lower():
            state.selected_fish = fish
            return fish_information(state)
    return choose_from_list(state)

@route
def fish_information(state: State) -> Page:
    """Consumes the current application state with a selected fish,
    producing a page showing its primary name, image, common names, and navigation buttons.

    Args:
        state (State): the current state containing selected_fish.

    Returns:
        Page: a Drafter Page displaying general information for the selected fish."""
    chosen_fish = state.selected_fish
    primary_name = chosen_fish.common_names[0]
    image_url = ""
    for fish1_object in fish_image_list:
        if fish1_object.name.lower() == primary_name.lower():
            image_url = fish1_object.url
            break
    return Page(state, [Header(primary_name),
                Image(image_url, width = 300),
                Div(Text("Common Names: " + ", ".join(chosen_fish.common_names))),
                Div(Button("Regulation Information", go_to_regulations),
                    Button("New Search", go_home))])

@route
def go_to_regulations(state: State) -> Page:
    """Consumes the current application state with a selected fish,
    producing a page displaying minimum/maximum size limits or harvest prohibition status.

    Args:
        state (State): the current state containing selected_fish.

    Returns:
        Page: a Drafter Page detailing size regulations and season navigation options."""
    fish = state.selected_fish
    primary_name = fish.common_names[0]
    if fish.min_size < 0:
        size_info = Text("Harvesting is PROHIBITED.")
    else:
        if fish.min_size == 0.0: 
            minimum = "No Minimum Size"
        else:
            minimum = str(fish.min_size)
        if fish.max_size == 999.9:
            maximum = "No Maximum Size"
        else:
            maximum = str(fish.max_size)
        size_info = Text("Minimum Size: " + minimum + " | " + "Maximum Size: " + maximum)
    
    return Page(state, [Header("Regulation Information: " + primary_name),
                size_info,
                LineBreak(),
                Text("Open Season:"),
                Button("Season Information", season_information),
                Button("Return to  Information", fish_information),
                Button("New Search", go_home)])
@route
def season_information(state: State) -> Page:
    """Consumes the current application state with a selected fish,
    producing a page listing all open fishing season date ranges for that species.

    Args:
        state (State): the current state containing selected_fish.

    Returns:
        Page: a Drafter Page displaying formatted open season ranges and return buttons."""
    fish = state.selected_fish
    primary_name = fish.common_names[0]
    content = [Header("Season Information: " + primary_name)]
    all_seasons = []
    for a_season in fish.season:
        season_start = a_season.first_month + " " + a_season.first_day
        season_end = a_season.last_month + " " + a_season.last_day
        season_session = season_start + " - " + season_end
        all_seasons.append(season_session)
    for s in all_seasons:
        content.append(Text(s))
    content.append(Button("Return to Regulations", go_to_regulations))
    content.append(Button("Return to  Information", fish_information))
    return Page(state, content)

@route
def go_home(state: State) -> Page:
    """Consumes the current application state and resets all search and selection fields
    back to their default initial values.

    Args:
        state (State): the current state of the application.

    Returns:
        Page: the cleared index home page."""
    state.fish_search = ""
    state.matching_fish = []
    state.selected_fish = NO_FISH
    state.current_page = "home"
    return index(state)

@route
def index(state: State) -> Page:
    """Consumes the current application state,
    producing the home search page with an optional no-match warning message.

    Args:
        state (State): the current state of the application.

    Returns:
        Page: the main search Page for Delaware ing Regulations."""
    content = [Header("Delaware ing Regulations and Information"),
                            Text("Full  Name: "),
                            TextBox("name_searched", state.fish_search),
                            Button("Search", fish_search_result)]
    
    if state.fish_search != "" and len(state.matching_fish) == 0:
        content.append(Div(Text("No fish found matching. Please type a new name.")))
    return Page(state, content)

TEST_WAHOO = (["Wahoo"], 0.0, 999.9, [Season("January", "1", "December", "31")])
TEST_COBIA = Fish(["Cobia"], 43.0, 999.9, [Season("June", "15", "September", "15")])
TEST_TAUTOG = Fish(["Tautog", "Blackfish"], 16.0, 999.9, [Season("January", "1", "May", "15"),
            Season("July", "1", "December", "31")])
TEST_MAKO = Fish(["Shortfin Mako Shark"], -999.9, 0.0, [Season("January", "1", "December", "31")])
TEST_STRIPED_BASS = Fish(["Striped Bass", "Rockfish"], 28.0, 31.0,
                    [Season("January", "1", "December", "31")])
TEST_BLUEGILL = Fish(["Bluegill"], 0.0, 999.9, [Season("January", "1", "December", "31")])
TEST_WALLEYE = Fish(["Walleye"], 15.0, 999.9, [Season("January", "1", "December", "31")])
TEST_BLACK_CRAPPIE = Fish(["Black Crappie"], 0.0, 999.9, [Season("January", "1", "December", "31")])
TEST_WHITE_CRAPPIE = Fish(["White Crappie"], 0.0, 999.9, [Season("January", "1", "December", "31")])

assert_equal(index(State("", [], NO_FISH, "home")), Page(State("", [], NO_FISH, "home"), [
        Header("Delaware Fishing Regulations and Information"),
        Text("Full Fish Name: "),
        TextBox("name_searched", ""),
        Button("Search", fish_search_result)]))
assert_equal(index(State("Unicorn", [], NO_FISH, "home")), Page(State("Unicorn", [], NO_FISH, "home"), [
        Header("Delaware Fishing Regulations and Information"),
        Text("Full Fish Name: "),
        TextBox("name_searched", "Unicorn"),
        Button("Search", fish_search_result),
        Div(Text("No fish found matching. Please type a new name."))]))
assert_equal(index(State("Wahoo", [TEST_WAHOO], TEST_WAHOO, "home")),
        Page(State("Wahoo", [TEST_WAHOO], TEST_WAHOO, "home"), [
        Header("Delaware Fishing Regulations and Information"),
        Text("Full Fish Name: "),
        TextBox("name_searched", "Wahoo"),
        Button("Search", fish_search_result)]))
assert_equal(fish_search_result(State("", [], NO_FISH, "home"), "Wahoo"),
        Page(State("Wahoo", [TEST_WAHOO], TEST_WAHOO, "home"), [
        Header("Wahoo"),
        Image("wahoo.jpg", width=300),
        Div(Text("Common Names: Wahoo")),
        Div(Button("Regulation Information", go_to_regulations),
            Button("New Search", go_home))]))

assert_equal(fish_search_result(State("", [], NO_FISH, "home"), "Wahoo"),
        Page(State("Wahoo", [TEST_WAHOO], TEST_WAHOO, "home"), [
        Header("Wahoo"),
        Image("wahoo.jpg", width=300),
        Div(Text("Common Names: Wahoo")),
        Div(Button("Regulation Information", go_to_regulations),
            Button("New Search", go_home))]))
assert_equal(fish_search_result(State("", [], NO_FISH, "home"), "Crappie"),
        Page(State("Crappie", [TEST_BLACK_CRAPPIE, TEST_WHITE_CRAPPIE], NO_FISH, "home"), [
        Header("Please Identify the Correct Fish"),
        Text("Type in the Correct Fish Below:"),
        Div(Text("Black Crappie"), LineBreak(), Image("black crappie.jpg")),
        Div(Text("White Crappie"), LineBreak(), Image("white crappie.jpg")),
        TextBox("chosen_name", ""),
        Button("Select Fish", select_chosen_fish),
        Button("Return Home", go_home)]))
assert_equal(fish_search_result(State("", [], NO_FISH, "home"), "Dragon"),
        Page(State("Dragon", [], NO_FISH, "home"), [
        Header("Delaware Fishing Regulations and Information"),
        Text("Full Fish Name: "),
        TextBox("name_searched", "Dragon"),
        Button("Search", fish_search_result),
        Div(Text("No fish found matching. Please type a new name."))]))

assert_equal(choose_from_list(State("Crappie", [TEST_BLACK_CRAPPIE, TEST_WHITE_CRAPPIE], NO_FISH, "home")),
        Page(State("Crappie", [TEST_BLACK_CRAPPIE, TEST_WHITE_CRAPPIE], NO_FISH, "home"), [
        Header("Please Identify the Correct Fish"),
        Text("Type in the Correct Fish Below:"),
        Div(Text("Black Crappie"), LineBreak(), Image("black crappie.jpg")),
        Div(Text("White Crappie"), LineBreak(), Image("white crappie.jpg")),
        TextBox("chosen_name", ""),
        Button("Select Fish", select_chosen_fish),
        Button("Return Home", go_home)]))
assert_equal(choose_from_list(State("Wahoo", [TEST_WAHOO], NO_FISH, "home")),
        Page(State("Wahoo", [TEST_WAHOO], NO_FISH, "home"), [
        Header("Please Identify the Correct Fish"),
        Text("Type in the Correct Fish Below:"),
        Div(Text("Wahoo"), LineBreak(), Image("wahoo.jpg")),
        TextBox("chosen_name", ""),
        Button("Select Fish", select_chosen_fish),
        Button("Return Home", go_home)]))
assert_equal(choose_from_list(State("", [], NO_FISH, "home")),
        Page(State("", [], NO_FISH, "home"), [
        Header("Please Identify the Correct Fish"),
        Text("Type in the Correct Fish Below:"),
        TextBox("chosen_name", ""),
        Button("Select Fish", select_chosen_fish),
        Button("Return Home", go_home)]))

assert_equal(select_chosen_fish(State("Crappie", [TEST_BLACK_CRAPPIE, TEST_WHITE_CRAPPIE], NO_FISH, "home"),
                                "Black Crappie"),
        Page(State("Crappie", [TEST_BLACK_CRAPPIE, TEST_WHITE_CRAPPIE], TEST_BLACK_CRAPPIE, "home"), [
        Header("Black Crappie"),
        Image("black crappie.jpg", width=300),
        Div(Text("Common Names: Black Crappie")),
        Div(Button("Regulation Information", go_to_regulations),
            Button("New Search", go_home))]))
assert_equal(select_chosen_fish(State("Crappie", [TEST_BLACK_CRAPPIE, TEST_WHITE_CRAPPIE], NO_FISH, "home"),
                                "white crappie"),
        Page(State("Crappie", [TEST_BLACK_CRAPPIE, TEST_WHITE_CRAPPIE], TEST_WHITE_CRAPPIE, "home"), [
        Header("White Crappie"),
        Image("white crappie.jpg", width=300),
        Div(Text("Common Names: White Crappie")),
        Div(Button("Regulation Information", go_to_regulations),
            Button("New Search", go_home))]))
assert_equal(select_chosen_fish(State("Crappie", [TEST_BLACK_CRAPPIE, TEST_WHITE_CRAPPIE], NO_FISH, "home"),
                                "Invalid Name"),
        Page(State("Crappie", [TEST_BLACK_CRAPPIE, TEST_WHITE_CRAPPIE], NO_FISH, "home"), [
        Header("Please Identify the Correct Fish"),
        Text("Type in the Correct Fish Below:"),
        Div(Text("Black Crappie"), LineBreak(), Image("black crappie.jpg")),
        Div(Text("White Crappie"), LineBreak(), Image("white crappie.jpg")),
        TextBox("chosen_name", ""),
        Button("Select Fish", select_chosen_fish),
        Button("Return Home", go_home)]))

assert_equal(fish_information(State("Wahoo", [TEST_WAHOO], TEST_WAHOO, "home")),
        Page(State("Wahoo", [TEST_WAHOO], TEST_WAHOO, "home"), [
        Header("Wahoo"),
        Image("wahoo.jpg", width=300),
        Div(Text("Common Names: Wahoo")),
        Div(Button("Regulation Information", go_to_regulations),
            Button("New Search", go_home))]))
assert_equal(fish_information(State("Tautog", [TEST_TAUTOG], TEST_TAUTOG, "home")),
        Page(State("Tautog", [TEST_TAUTOG], TEST_TAUTOG, "home"), [
        Header("Tautog"),
        Image("tautog.jpg", width=300),
        Div(Text("Common Names: Tautog, Blackfish")),
        Div(Button("Regulation Information", go_to_regulations),
            Button("New Search", go_home))]))
assert_equal(fish_information(State("Striped Bass", [TEST_STRIPED_BASS], TEST_STRIPED_BASS, "home")),
        Page(State("Striped Bass", [TEST_STRIPED_BASS], TEST_STRIPED_BASS, "home"), [
        Header("Striped Bass"),
        Image("striped bass.jpg", width=300),
        Div(Text("Common Names: Striped Bass, Rockfish")),
        Div(Button("Regulation Information", go_to_regulations),
            Button("New Search", go_home))]))

assert_equal(go_to_regulations(State("Mako", [TEST_MAKO], TEST_MAKO, "home")),
        Page(State("Mako", [TEST_MAKO], TEST_MAKO, "home"), [
        Header("Regulation Information: Shortfin Mako Shark"),
        Text("Harvesting is PROHIBITED."),
        LineBreak(),
        Text("Open Season:"),
        Button("Season Information", season_information),
        Button("Return to Fish Information", fish_information),
        Button("New Search", go_home)]))
assert_equal(go_to_regulations(State("Bluegill", [TEST_BLUEGILL], TEST_BLUEGILL, "home")),
        Page(State("Bluegill", [TEST_BLUEGILL], TEST_BLUEGILL, "home"), [
        Header("Regulation Information: Bluegill"),
        Text("Minimum Size: No Minimum Size | Maximum Size: No Maximum Size"),
        LineBreak(),
        Text("Open Season:"),
        Button("Season Information", season_information),
        Button("Return to Fish Information", fish_information),
        Button("New Search", go_home)]))
assert_equal(go_to_regulations(State("Striped Bass", [TEST_STRIPED_BASS], TEST_STRIPED_BASS, "home")),
        Page(State("Striped Bass", [TEST_STRIPED_BASS], TEST_STRIPED_BASS, "home"), [
        Header("Regulation Information: Striped Bass"),
        Text("Minimum Size: 28.0 | Maximum Size: 31.0"),
        LineBreak(),
        Text("Open Season:"),
        Button("Season Information", season_information),
        Button("Return to Fish Information", fish_information),
        Button("New Search", go_home)]))

assert_equal(season_information(State("Walleye", [TEST_WALLEYE], TEST_WALLEYE, "home")),
        Page(State("Walleye", [TEST_WALLEYE], TEST_WALLEYE, "home"), [
        Header("Season Information: Walleye"),
        Text("January 1 - December 31"),
        Button("Return to Regulations", go_to_regulations),
        Button("Return to Fish Information", fish_information)]))
assert_equal(season_information(State("Cobia", [TEST_COBIA], TEST_COBIA, "home")),
        Page(State("Cobia", [TEST_COBIA], TEST_COBIA, "home"), [
        Header("Season Information: Cobia"),
        Text("June 15 - September 15"),
        Button("Return to Regulations", go_to_regulations),
        Button("Return to Fish Information", fish_information)]))
assert_equal(season_information(State("Tautog", [TEST_TAUTOG], TEST_TAUTOG, "home")),
        Page(State("Tautog", [TEST_TAUTOG], TEST_TAUTOG, "home"), [
        Header("Season Information: Tautog"),
        Text("January 1 - May 15"),
        Text("July 1 - December 31"),
        Button("Return to Regulations", go_to_regulations),
        Button("Return to Fish Information", fish_information)]))

assert_equal(go_home(State("Wahoo", [TEST_WAHOO], TEST_WAHOO, "details")),
        Page(State("", [], NO_FISH, "home"), [
        Header("Delaware Fishing Regulations and Information"),
        Text("Full Fish Name: "),
        TextBox("name_searched", ""),
        Button("Search", fish_search_result)]))
assert_equal(go_home(State("Invalid", [], NO_FISH, "home")),
        Page(State("", [], NO_FISH, "home"), [
        Header("Delaware Fishing Regulations and Information"),
        Text("Full Fish Name: "),
        TextBox("name_searched", ""),
        Button("Search", fish_search_result)]))
assert_equal(go_home(State("", [], NO_FISH, "home")),
        Page(State("", [], NO_FISH, "home"), [
        Header("Delaware Fishing Regulations and Information"),
        Text("Full Fish Name: "),
        TextBox("name_searched", ""),
        Button("Search", fish_search_result)]))



initial_state = State("", [], NO_FISH, "home")
start_server(initial_state)
