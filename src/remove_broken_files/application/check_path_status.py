import requests

class CheckPathStatusUseCase:
    def __init__(self):
        self.broken_files_id = []


    def execute(self, file):
            try:
                response = requests.get(file['path'])
                if response.status_code == 200:
                    print(f"file exists: {file['path']}")
                else:
                    print(f"file is broken: {file['path']}")
                    self.broken_files_id.append(file['id'])
            except requests.RequestException as e:
                print(f"Error accessing file {file['path']}: {e}")
                self.broken_files_id.append(file['id'])

    def get_broken_paths(self):
        return self.broken_files_id