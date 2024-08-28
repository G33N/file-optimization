from shared.infrastructure.database_repository import DatabaseRepository

class CheckPathPriorityUseCase:
    def __init__(self, database_repository):
        self.database_repository: DatabaseRepository = database_repository

    def execute(self, path):
        self.database_repository.connect()

        query = "SELECT listing_images.id as image_id, file.id as file_id FROM file LEFT JOIN listing_images ON file.id = listing_images.\"fileId\" WHERE listing_images.priority = 1 AND file.path = %s"
        imageRaw = self.database_repository.execute_query(query, (path,))
        
        self.database_repository.close()

        image = [image[0] for image in imageRaw]

        return len(image) > 0