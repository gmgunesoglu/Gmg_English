# load_data.py
from database import create_reading_unit, create_reading_text, create_reading_quest


def load_sample_data():
    # ReadingUnit verisi ekleniyor
    unit1 = create_reading_unit("Unit 1")
    unit2 = create_reading_unit("Unit 2")

    # ReadingText verisi ekleniyor
    text1 = create_reading_text("Title 1", "Context for unit 1", unit1.id)
    text2 = create_reading_text("Title 2", "Context for unit 2", unit2.id)

    # ReadingQuest verisi ekleniyor
    create_reading_quest(
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
    load_sample_data()
