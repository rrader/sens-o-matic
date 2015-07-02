from peewee import *

db = SqliteDatabase('sensors.db')


class Sensor(Model):
    name = CharField()
    value = CharField()
    timestamp = DateField()

    class Meta:
        database = db  # This model uses the "people.db" database.


def get_last_record(sensor_name):
    records = list(Sensor.select(Sensor.value).
                   where(Sensor.name == sensor_name).
                   order_by(Sensor.timestamp.desc()).
                   limit(1))
    if records:
        return records[0]


if __name__ == "__main__":
  db.create_tables([Sensor])
