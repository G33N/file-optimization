from shared.infrastructure.database_repository import DatabaseRepository

class UpdateImagePriorityUseCase:
    def __init__(self, database_repository):
        self.database_repository: DatabaseRepository = database_repository

    def execute(self):
        self.database_repository.connect()

        print("Updating image priority...")

        try:
            query = "SELECT id, \"listingId\", priority FROM listing_images"
            images = self.database_repository.execute_query(query)
            
            listing_images = {}
            for image in images:
                image_id, listing_id, priority = image
                if listing_id not in listing_images:
                    listing_images[listing_id] = []
                listing_images[listing_id].append((image_id, priority))
            
            for listing_id, images in listing_images.items():
                has_priority_1 = any(priority == 1 for _, priority in images)
                
                if not has_priority_1:
                    image_to_update = images[0][0]
                    update_query = """
                        UPDATE listing_images
                        SET priority = 1
                        WHERE id = %s
                    """
                    self.database_repository.execute_query(update_query, (image_to_update,))
        finally:
            print("Image priority updated.")
            self.database_repository.close()