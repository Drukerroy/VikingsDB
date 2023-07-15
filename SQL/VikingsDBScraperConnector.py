import psycopg2
import os
import pandas as pd


class VikingsDBScraperConnector():
    def __init__(self):
        self.conn = psycopg2.connect(
            host='dpg-ciohtolph6elhbt6oru0-a',
            dbname='vikingsdatabase',
            user='vikingsdatabase_user',
            password='ehYdAjcULaUASBTNLJ1iOx1tkqRvAR4Q',
            port=5432
        )

    def close_conn(self):
        self.conn.close()

    def insert_character_and_actor(self, data):
        try:
            cursor = self.conn.cursor()

            data_list = []
            for cast_show in data.values():
                for character_name, info in cast_show.items():
                    # Extract character data from the dictionary
                    character_first_name = character_name.split(' ', 1)[0] if ' ' in character_name else character_name
                    character_last_name = character_name.split(' ', 1)[1] if ' ' in character_name else None
                    character_description = info['Character Description'] if 'Character Description' in info.keys() else None
                    character_image = info['Image URL'] if 'Image URL' in info.keys() else None
                    actor_first_name = info['Actor Name'].split(' ', 1)[0] if ' ' in info['Actor Name'] else info['Actor Name']
                    actor_last_name = info['Actor Name'].split(' ', 1)[1] if ' ' in info['Actor Name'] else None
                    actor_description = info['Actor Description'] if 'Actor Description' in info.keys() else None
                    tv_show = info['TV Show']

                    data_list.append([character_first_name, character_last_name, character_description, character_image,
                                      actor_first_name, actor_last_name, actor_description, tv_show])

                    actor_query = """
                        INSERT INTO actor (firstname, lastname, description)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (firstname, lastname)
                        DO UPDATE SET description = EXCLUDED.description
                        RETURNING actorid
                    """
                    cursor.execute(actor_query, (actor_first_name, actor_last_name, actor_description))
                    actor_id = cursor.fetchone()[0]

                    character_query = """
                        INSERT INTO character (firstname, lastname, description, imagesrc, tvshow, actorid)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (actorid) DO UPDATE
                        SET firstname = EXCLUDED.firstname,
                            lastname = EXCLUDED.lastname,
                            description = EXCLUDED.description,
                            imagesrc = EXCLUDED.imagesrc,
                            tvshow = EXCLUDED.tvshow
                        RETURNING characterid
                    """
                    cursor.execute(character_query, (character_first_name, character_last_name, character_description, character_image, tv_show, actor_id))
                    character_id = cursor.fetchone()[0]

                    print(f'Character with id {character_id} and actor with id {actor_id} was created or updated')

            df = pd.DataFrame(data_list,
                              columns=['Character First Name', 'Character Last Name', 'Character Description',
                                       'Character Image', 'Actor First Name', 'Actor Last Name', 'Actor Description',
                                       'TV Show'])
            df.insert(0, 'ID', range(1, 1 + len(df)))

            df.to_csv("../scraper/vikings_data.csv", index=False)

            self.conn.commit()
            cursor.close()

        except psycopg2.Error as e:
            print(f"Error inserting or updating character and actor: {e}")


vikings_db_connector = VikingsDBScraperConnector()
