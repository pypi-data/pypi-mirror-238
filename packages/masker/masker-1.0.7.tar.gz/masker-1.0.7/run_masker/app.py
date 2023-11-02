from application.core.parser_data import parse_data
from application.core.jobs.get_masked_or_deleted_db import delete_rows_from_db, mask_db
from application.core.parser_data import get_all_columns_by_query


def main():
    command_line_args, conn = parse_data()
    if conn is not None:
        if command_line_args.action == 'delete':
            if command_line_args.table and command_line_args.percentage:
                delete_rows_from_db(conn, command_line_args.table, command_line_args.percentage)
            else:
                print("No table or percentage data to be deleted has been entered")
        elif command_line_args.action == 'mask':
            if command_line_args.table:
                if not command_line_args.columns:
                    mask_db(conn, command_line_args.table, get_all_columns_by_query(command_line_args.table, conn))
                else:
                    mask_db(conn, command_line_args.table, command_line_args.columns)
            else:
                print("No table to be deleted has been entered")

        else:
            print("Invalid Action: ", command_line_args.action)
    else:
        print('Could not connect to database')


if __name__ == "__main__":
    main()
