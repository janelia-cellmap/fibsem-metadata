from fibsem_metadata.database_sqa import create_db_and_tables
import fibsem_metadata.schemas.views as schemas

if __name__ == '__main__':
    create_db_and_tables(wipe=True)
