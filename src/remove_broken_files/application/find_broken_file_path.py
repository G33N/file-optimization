from shared.infrastructure.database_repository import DatabaseRepository

class FindBrokenFilePathUseCase:
    def __init__(self, database_repository):
        self.databe_repository: DatabaseRepository = database_repository

    def execute(self):
        self.databe_repository.connect()
        result = self.databe_repository.execute_query("SELECT id, path FROM file")
        self.databe_repository.close()
        files = [{'id': row[0], 'path': row[1]} for row in result]
        return files