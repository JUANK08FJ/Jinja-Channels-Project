import sqlite3


def get_channels():
    conn = sqlite3.connect("tv_channels.sqlite")
    sql = "SELECT * FROM channels;"
    cursor = conn.execute(sql)
    channels = []
    for row in cursor:
        channel = {"channel_id": row[0], "name": row[1], "image_url": row[2], "founder": row[3], "launch_date": row[4],
                   "description": row[5]}
        channels.append(channel)
    conn.close()

    return channels


def channel_creation(name, image_url, founder, launch_date, description):
    conn = sqlite3.connect("tv_channels.sqlite")
    sql = "INSERT INTO channels (name, image_url, founder, launch_date, description) VALUES (?,?,?,?,?)"

    values = [name, image_url, founder, launch_date, description]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def channel_deletion(channel_id):
    conn = sqlite3.connect("tv_channels.sqlite")
    sql = "DELETE FROM channels WHERE channel_id == ?"

    values = [channel_id]

    conn.execute(sql, values)
    conn.commit()
    conn.close()


def channel_modification(name, image_url, founder, launch_date, description, channel_id):
    conn = sqlite3.connect("tv_channels.sqlite")
    sql = "UPDATE channels SET name = ?, image_url = ?, founder = ?, launch_date = ?, description = ?  WHERE channel_id = ?"

    values = [name, image_url, founder, launch_date, description, channel_id]

    conn.execute(sql, values)
    conn.commit()
    conn.close()


def get_shows():
    conn = sqlite3.connect("tv_channels.sqlite")
    sql = "SELECT * FROM animated_shows;"
    cursor = conn.execute(sql)
    shows = []
    for row in cursor:
        show = {"animation_id": row[0], "title": row[1], "image_url": row[2], "release_date": row[3],
                "director": row[4], "episodes": row[5], "channel_id": row[6], "synopsis": row[7]}
        shows.append(show)
    conn.close()

    return shows


def animation_creation(title, image_url, release_date, director, episodes, channel_id, synopsis):
    conn = sqlite3.connect("tv_channels.sqlite")
    sql = "INSERT INTO animated_shows (title, image_url, release_date, director, episodes, channel_id, synopsis) VALUES (?,?,?,?,?,?,?)"

    values = [title, image_url, release_date, director, episodes, channel_id, synopsis]
    conn.execute(sql, values)
    conn.commit()
    conn.close()


def animation_deletion(animation_id):
    conn = sqlite3.connect("tv_channels.sqlite")
    sql = "DELETE FROM animated_shows WHERE animation_id == ?"

    values = [animation_id]

    conn.execute(sql, values)
    conn.commit()
    conn.close()


def animation_modification(title, image_url, release_date, director, episodes, channel_id, synopsis, animation_id):
    conn = sqlite3.connect("tv_channels.sqlite")
    sql = "UPDATE animated_shows SET title = ?, image_url = ?, release_date = ?, director = ?, episodes = ?, channel_id = ?, synopsis = ? WHERE animation_id = ?"

    values = [title, image_url, release_date, director, episodes, channel_id, synopsis, animation_id]

    conn.execute(sql, values)
    conn.commit()
    conn.close()
