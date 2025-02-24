# init_data.py
from database import get_session, init_db
from models import ReadingUnit, ReadingText, ReadingQuest


def create_reading_unit(session, name):
    unit = ReadingUnit(name=name)
    session.add(unit)
    session.commit()
    session.refresh(unit)
    return unit


def create_reading_text(session, title, context, reading_unit_id):
    text = ReadingText(title=title, context=context, reading_unite_id=reading_unit_id)
    session.add(text)
    session.commit()
    session.refresh(text)
    return text


def create_reading_quest(session, quest, option_a, option_b, option_c, option_d, correct_option, justification,
                         reading_text_id):
    quest_entry = ReadingQuest(
        quest=quest,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_option=correct_option,
        justification=justification,
        reading_text_id=reading_text_id
    )
    session.add(quest_entry)
    session.commit()
    session.refresh(quest_entry)
    return quest_entry


def load_sample_data():
    # Veritabanı oturumu başlatılıyor
    with next(get_session()) as session:
        # ReadingUnit verisi ekleniyor
        unit1 = create_reading_unit(session, "Unit 1")
        unit2 = create_reading_unit(session, "Unit 2")

        # ReadingText verisi ekleniyor
        text1 = create_reading_text(session, "Title 1", "Context for unit 1", unit1.id)
        text2 = create_reading_text(session, "Title 2", "Context for unit 2", unit2.id)

        # ReadingQuest verisi ekleniyor
        create_reading_quest(
            session,
            quest="What is the capital of Turkey?",
            option_a="Istanbul",
            option_b="Ankara",
            option_c="Izmir",
            option_d="Antalya",
            correct_option="B",
            justification="Ankara is the capital of Turkey.",
            reading_text_id=text1.id
        )

        create_reading_quest(
            session,
            quest="What is the capital of France?",
            option_a="Paris",
            option_b="London",
            option_c="Berlin",
            option_d="Rome",
            correct_option="A",
            justification="Paris is the capital of France.",
            reading_text_id=text2.id
        )

        print("Sample data has been loaded successfully!")


if __name__ == "__main__":
    init_db()  # Veritabanını başlat
    load_sample_data()  # Örnek verileri yükle
