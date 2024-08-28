from shared.infrastructure.database_repository import DatabaseRepository

class RemoveBrokenFilePathUseCase:
    def __init__(self, database_repository):
        self.database_repository: DatabaseRepository = database_repository

    def execute(self, files):
        print("Removing broken file paths...")
        self.database_repository.connect()

        if not files:
            print("No file IDs to process.")
            return

        file_placeholders = ','.join(['%s'] * len(files))
        query = f"SELECT id FROM listing_images WHERE listing_images.\"fileId\" IN ({file_placeholders})"

        listing_images = self.database_repository.execute_query(query, tuple(files))

        image_ids = [image[0] for image in listing_images]

        if not image_ids:
            print("No images to delete.")

        image_placeholders = ','.join(['%s'] * len(image_ids))
        self.database_repository.execute_query(f"DELETE FROM listing_images WHERE listing_images.id IN ({image_placeholders})", tuple(image_ids))
        self.database_repository.execute_query(f"DELETE FROM file WHERE file.id IN ({file_placeholders})", tuple(files))

        print(f"Broken file paths removed. {files}" )

        self.database_repository.close()