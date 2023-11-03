import re
from sqlalchemy import text


def delete_rows_from_db(connection, table_name, percentage):
    try:
        total_rows = connection.execute(text(f'SELECT COUNT(*) FROM {table_name}')).scalar()
        rows_to_delete = int(total_rows * (percentage / 100))
        delete_query = text(
            f'DELETE FROM {table_name} WHERE ctid IN (SELECT ctid FROM {table_name} ORDER BY RANDOM() LIMIT :limit)'
        ).bindparams(limit=rows_to_delete)
        connection.execute(delete_query)
        print(f"{percentage}% of data deleted from the {table_name} table.")
        connection.commit()
        connection.close()
    except Exception as e:
        print(f"Error: {e}")


def mask_data(connection, table_name, columns):
    try:
        for column in columns:
            max_length_query = text(f'SELECT MAX(LENGTH({column})) FROM {table_name}')
            max_length = connection.execute(max_length_query).scalar()
            mask_query = text(f'UPDATE {table_name} SET {column} = REPEAT(\'*\', {max_length})')
            connection.execute(mask_query)

        connection.commit()
        connection.close()
        print(f"Data in columns {', '.join(columns)} has been masked with '*' up to the maximum character length.")
    except Exception as e:
        print(f"Error: {e}")


def replace_email(match):
    email = match.group(0)
    if len(email) > 2:
        parts = email.split("@")
        username = parts[0]
        new_email = email[0] + '*' * (len(username) - 2) + username[-1] + '@' + parts[1]
        return new_email
    else:
        return email


def replace_phone_number(match):
    phone = match.group(0)
    return phone[:-4] + '****'


def replace_password(match):
    username = match.group(1)
    if len(match.group(2)) > 5:
        return f"{username}******"
    else:
        return f"{username}{match.group(2)}"


def replace_url(match):
    return 'https://*****.com/***'


def replace_credit_card_number(match):
    credit_card_number = match.group(0)
    return credit_card_number[:4] + '*' * (len(credit_card_number) - 8) + credit_card_number[
                                                                          len(credit_card_number) - 4:len(
                                                                              credit_card_number)]


def replace_birth_date(match):
    return re.sub(r'\d', '*', match.group())


def mask_db(connection, table_name, columns, chunk_size=10):
    try:
        tc_pattern = re.compile(r'\b(\d{4})[-.\s]?(\d{3})[-.\s]?(\d{4})\b')
        credit_card_pattern = re.compile(r'\b4[0-9]{12}(?:[0-9]{3})?\b')
        email_pattern = re.compile(r'\b[A-Za-z0-9._*%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        phone_pattern = re.compile(r'\b(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})\b')
        password_pattern = re.compile(r'(\b[A-Za-z0-9_-]+:)\s*\b([A-Za-z0-9_-]+)\b')
        url_pattern = re.compile(
            r'(https?://(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]['
            r'a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?://(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,'
            r'}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
        birth_date_pattern = re.compile(r"(0[1-9]|[12][0-9]|3[01])[-/.](0[1-9]|1[012])[-/.](19|20)\d\d")

        total_rows = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()

        for column in columns:

            for offset in range(0, total_rows, chunk_size):
                query = text(
                    f"SELECT id, {column} FROM {table_name} ORDER BY id LIMIT {chunk_size} OFFSET {offset}"
                )
                id_and_column_data = connection.execute(query).fetchall()

                for tuple_data in id_and_column_data:
                    row_id, old_value = tuple_data

                    regenerated_value = email_pattern.sub(replace_email, old_value)
                    regenerated_value = phone_pattern.sub(replace_phone_number, regenerated_value)
                    regenerated_value = password_pattern.sub(replace_password, regenerated_value)
                    regenerated_value = tc_pattern.sub(replace_phone_number, regenerated_value)
                    regenerated_value = credit_card_pattern.sub(replace_credit_card_number, regenerated_value)
                    regenerated_value = url_pattern.sub(replace_url, regenerated_value)
                    regenerated_value = birth_date_pattern.sub(replace_birth_date, regenerated_value)

                    update_query = text(
                        f"UPDATE {table_name} SET {column} = :regenerated_value WHERE id = :row_id"
                    )
                    connection.execute(update_query, {"regenerated_value": regenerated_value, "row_id": row_id})
                    connection.commit()
                print(f"Updated {chunk_size} rows in {table_name} for {column}, offset: {offset}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()
