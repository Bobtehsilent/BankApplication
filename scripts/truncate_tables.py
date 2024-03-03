from sqlalchemy import text

def truncate_tables(tables, session):
    """
    Truncate given tables using a SQLAlchemy session for MySQL database.

    :param tables: A list of table model classes to be truncated.
    :param session: The SQLAlchemy session.
    """
    session.execute(text('SET FOREIGN_KEY_CHECKS=0;'))
    try:
        for table in tables:
            session.execute(text(f'TRUNCATE TABLE {table.__tablename__};'))
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Failed to truncate tables: {e}")
    finally:
        # Re-enable foreign key constraint checking
        session.execute(text('SET FOREIGN_KEY_CHECKS=1;'))
        session.close()

    print("Tables truncated successfully.")