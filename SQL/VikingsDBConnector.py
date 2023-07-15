from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_


class VikingsDBConnector:
    def __init__(self):
        self.db = SQLAlchemy()
        self.actor = ''
        self.character = ''

    def get_joined_tables(self):
        from webapp.models.Actor import Actor
        from webapp.models.Character import Character
        self.actor = Actor
        self.character = Character

        joined_table = self.db.session.query(Character, Actor).join(Actor).all()

        return joined_table

    def get_filtered_data(self, search_query, sort_option, category_option,
                          character_has_last_name, character_has_description,
                          actor_has_description, character_has_image):
        query = self.db.session.query(self.character, self.actor).join(self.actor)

        # Apply filtering based on the form data

        # Search query
        if search_query:
            query = query.filter(
                or_(
                    self.character.firstname.ilike(f"%{search_query}%"),
                    self.character.lastname.ilike(f"%{search_query}%"),
                    self.actor.firstname.ilike(f"%{search_query}%"),
                    self.actor.lastname.ilike(f"%{search_query}%")
                )
            )

        # Sort option
        if sort_option == "name":
            query = query.order_by(self.character.firstname, self.character.lastname)
        elif sort_option == "actor":
            query = query.order_by(self.actor.firstname, self.actor.lastname)
        elif sort_option == "tv-show":
            query = query.order_by(self.character.tvshow.desc())

        # Category option
        if category_option and category_option != "All":
            query = query.filter(self.character.tvshow == category_option)

        # Character has last name
        if character_has_last_name:
            query = query.filter(self.character.lastname != None)

        # Character has description
        if character_has_description:
            query = query.filter(self.character.description != None)

        # Actor has description
        if actor_has_description:
            query = query.filter(self.actor.description != None)

        # Character has image
        if character_has_image:
            query = query.filter(self.character.imagesrc != None)

        filtered_data = query.all()

        return filtered_data

    def get_character_page_info(self, character_first_name, actor_first_name, tv_show):
        joined_table = self.db.session.query(self.character, self.actor).join(self.actor).filter(
            self.character.firstname == character_first_name,
            self.actor.firstname == actor_first_name,
            self.character.tvshow == str(tv_show)
        ).all()

        return joined_table


vikings_db = VikingsDBConnector()
