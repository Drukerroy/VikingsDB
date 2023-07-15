from flask import Blueprint, render_template, request
from SQL.VikingsDBConnector import vikings_db
from sqlalchemy.sql import text


views = Blueprint("views", __name__, static_folder="static", template_folder="templates")


@views.route("/", methods=['POST', 'GET'])
def index():
    form_state = {
        'search': '',
        'sort': '',
        'category': '',
        'group1-option1': False,
        'group2-option1': False,
        'group2-option2': False,
        'group2-option3': False
    }

    if request.method == 'POST':
        search_query = request.form['search'] if request.form['search'] else None
        sort_option = request.form['sort'] if request.form['sort'] else None
        tvshow_option = request.form['tvshow'] if request.form['tvshow'] else None
        character_has_last_name = True if 'group1-option1' in request.form else False
        character_has_description = True if 'group2-option1' in request.form else False
        actor_has_description = True if 'group2-option2' in request.form else False
        character_has_image = True if 'group2-option3' in request.form else False

        filtered_data = vikings_db.get_filtered_data(search_query, sort_option, tvshow_option,
                                                     character_has_last_name, character_has_description,
                                                     actor_has_description, character_has_image)
        form_state = {
            'search': search_query,
            'sort': sort_option,
            'tvshow': tvshow_option,
            'group1-option1': character_has_last_name,
            'group2-option1': character_has_description,
            'group2-option2': actor_has_description,
            'group2-option3': character_has_image
        }

    else:
        filtered_data = vikings_db.get_joined_tables()

    return render_template("index.html", table=filtered_data, form_state=form_state)


@views.route("character/<string:character_first_name>_<string:tv_show>_<string:actor_first_name>")
def character(character_first_name, tv_show, actor_first_name):
    character_info = vikings_db.get_character_page_info(character_first_name, actor_first_name, tv_show)

    character_name = character_info[0].Character.firstname + ' ' + character_info[0].Character.lastname \
        if character_info[0].Character.lastname else character_info[0].Character.firstname

    image_src = character_info[0].Character.imagesrc if character_info[0].Character.imagesrc else 'https://placehold.co/600x400.png'

    character_dict = {
        'Character Name': character_name,
        'Actor Name': character_info[0].Actor.firstname + ' ' + character_info[0].Actor.lastname,
        'Character Description': character_info[0].Character.description,
        'Actor Description': character_info[0].Actor.description,
        'Image Src': image_src
    }

    return render_template("character.html", data=character_dict)
