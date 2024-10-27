# Class representing a directory node in the directory tree
class Directory:
    def __init__(self, name):
        self.name = name  # Directory name
        self.subdirectories = {}  # Dictionary to hold subdirectories

    # Method to add a subdirectory at a given path
    def add_subdirectory(self, path_parts):
        if not path_parts:  # Base case: no more parts to process
            return
        part = path_parts[0]  # Get the current directory name
        if part not in self.subdirectories:  # If directory doesn't exist, create it
            self.subdirectories[part] = Directory(part)
        # Recursively add subdirectories for the remaining path
        self.subdirectories[part].add_subdirectory(path_parts[1:])

    # Method to move a subdirectory from one location to another
    def move_subdirectory(self, src, dest):
        if src in self.subdirectories:
            # Move subdirectory from 'src' to 'dest' if it exists
            self.subdirectories[dest] = self.subdirectories.pop(src)

    # Method to delete a subdirectory at a given path
    def delete_subdirectory(self, path_parts):
        if len(path_parts) == 1:
            # If it's the last part of the path, attempt to delete it
            if path_parts[0] in self.subdirectories:
                del self.subdirectories[path_parts[0]]
                return True  # Return success
            else:
                return False  # Directory not found
        else:
            # Recursively traverse the directory tree to find the subdirectory to delete
            next_part = path_parts[0]
            if next_part in self.subdirectories:
                return self.subdirectories[next_part].delete_subdirectory(path_parts[1:])
            else:
                return False  # Directory not found

    # Method to print the directory structure
    def list_structure(self, level=0):
        indent = '  ' * level  # Create indentation based on the directory level
        print(f"{indent}{self.name}")  # Print the current directory name
        # Recursively print subdirectories in alphabetical order
        for subdir in sorted(self.subdirectories.values(), key=lambda x: x.name):
            subdir.list_structure(level + 1)

    # Method to find a subdirectory at a given path
    def find_subdirectory(self, path_parts):
        if not path_parts:  # Base case: no more parts to process
            return self
        part = path_parts[0]
        if part in self.subdirectories:  # If the directory exists, continue searching
            return self.subdirectories[part].find_subdirectory(path_parts[1:])
        else:
            return None  # Directory not found


# Class to manage the overall directory tree
class DirectoryTree:
    def __init__(self):
        self.root = Directory('')  # Initialize with a root directory

    # Method to create a new directory at the given path
    def create(self, path):
        path_parts = path.split('/')  # Split path by '/'
        self.root.add_subdirectory(path_parts)  # Add subdirectory to the tree
        print(f"CREATE {path}")  # Output the command

    # Method to move a directory from src to dest
    def move(self, src, dest):
        src_parts = src.split('/')  # Split src path by '/'
        dest_parts = dest.split('/')  # Split dest path by '/'

        # Find source directory and destination directory
        src_dir = self.root.find_subdirectory(src_parts[:-1])
        dest_dir = self.root.find_subdirectory(dest_parts)

        if src_dir and dest_dir:  # If both directories are found
            src_dir.move_subdirectory(src_parts[-1], src_parts[-1])  # Remove from src
            dest_dir.subdirectories[src_parts[-1]] = src_dir.subdirectories[src_parts[-1]]  # Add to dest
            print(f"MOVE {src} {dest}")  # Output the command

    # Method to delete a directory at the given path
    def delete(self, path):
        path_parts = path.split('/')  # Split path by '/'
        if not self.root.delete_subdirectory(path_parts):  # Try deleting the directory
            # If deletion fails, output an error message
            print(f"Cannot delete {path} - {path_parts[0]} does not exist")
        else:
            print(f"DELETE {path}")  # Output the command

    # Method to print the current directory structure
    def list_tree(self):
        print("LIST")  # Output the command
        self.root.list_structure()  # List the directory structure


# Main function to execute the script
def main():
    # List of commands to be executed
    commands = [
        "CREATE fruits",
        "CREATE vegetables",
        "CREATE grains",
        "CREATE fruits/apples",
        "CREATE fruits/apples/fuji",
        "LIST",
        "CREATE grains/squash",
        "MOVE grains/squash vegetables",
        "CREATE foods",
        "MOVE grains foods",
        "MOVE fruits foods",
        "MOVE vegetables foods",
        "LIST",
        "DELETE fruits/apples",
        "DELETE foods/fruits/apples",
        "LIST"
    ]

    tree = DirectoryTree()  # Initialize a new DirectoryTree instance

    # Process each command
    for command in commands:
        parts = command.split()  # Split command into parts
        action = parts[0]  # Get the action (CREATE, MOVE, DELETE, LIST)

        if action == "CREATE":
            tree.create(parts[1])  # Call create method with the path
        elif action == "MOVE":
            tree.move(parts[1], parts[2])  # Call move method with src and dest
        elif action == "DELETE":
            tree.delete(parts[1])  # Call delete method with the path
        elif action == "LIST":
            tree.list_tree()  # Call list method


# Run the script if executed directly
if __name__ == "__main__":
    main()
