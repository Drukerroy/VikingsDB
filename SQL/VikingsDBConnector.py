from flask_sqlalchemy import SQLAlchemy


class VikingsQueries:
    def __init__(self):
        self.db = SQLAlchemy()

    def get_joined_table(self):
        pass

    def update_results(self):
        pass

    def insert_entities(self, data):
        print('here')
        from webapp.models.Actor import Actor
        from webapp.models.Character import Character

        for tv_show, cast in data.items():
            for character_name, info in cast.items():

                # Create an actor instance
                new_actor = Actor(
                    first_name=info['Actor Name'].split(' ', 1)[0] if ' ' in info['Actor Name'] else info['Actor Name'],
                    last_name=info['Actor Name'].split(' ', 1)[1] if ' ' in info['Actor Name'] else None,
                    description=info['Actor Description'] if 'Actor Description' in info.keys() else None
                )
                self.db.session.add(new_actor)

                # Create a character instance
                new_character = Character(first_name=character_name.split(' ', 1)[0] if ' ' in character_name else character_name,
                                          last_name=character_name.split(' ', 1)[0] if ' ' in character_name else None,
                                          description=info['Character Description'] if 'Character Description' in info.keys() else None,
                                          tv_show=info['TV Show'],
                                          image_src=info['Image URL'] if 'Image URL' in info.keys() else None,
                                          actor=new_actor)
                self.db.session.add(new_character)

                self.db.session.commit()


vikings_db = VikingsQueries()
