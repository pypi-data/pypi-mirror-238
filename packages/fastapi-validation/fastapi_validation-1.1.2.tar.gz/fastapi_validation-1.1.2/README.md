# FastAPI Validation

FastAPI Validation support both SQLAlchemy for sql database and BeanieODM for nosql Database.
To use the @Exists and @Unique decorator we need to set global-variable for the database_type
Check the sample code below

## For SQL Database using SQLAlchemy as ORM

```python
from fastapi_validation import DatabaseTypeEnum

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, pool_size=50, max_overflow=100)
global_db_session: Session = sessionmaker(
    autoflush=False, autobegin=True, bind=engine, join_transaction_mode='rollback_only'
)()
def run_with_global_session(callback):
    try:
        return callback(global_db_session)
    except Exception as e:
        global_db_session.rollback()
        raise e

GlobalVariable.set('run_with_global_session', run_with_global_session)
GlobalVariable.set('database_type', DatabaseTypeEnum.SQL)
```

## For Nosql Database using Beanie as ODM

```python
GlobalVariable.set('database_type', DatabaseTypeEnum.NOSQL) # We can skip this line because the defautl database_type is SQL

```
