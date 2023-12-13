import uuid

from schemas.reservation import DayReservations

CSV_DATA_DIR = "static/data/"


def create_csv_from_reservations_list(
    reservations: list[DayReservations],
) -> str:
    file_name = f"{uuid.uuid4()}.csv"
    with open(f"{CSV_DATA_DIR}{file_name}", "w") as file:
        csv = _get_csv_string_from_reservations(reservations)
        file.write(csv)

    return file_name


def _get_csv_string_from_reservations(
    reservations: list[DayReservations],
) -> str:
    csv = "Night,Count\n"
    for day in reservations:
        night = f"{day.date.day}/{day.date.month}/{day.date.year}"
        count = day.count
        csv += f"{night},{count}\n"

    return csv
