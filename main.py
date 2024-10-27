class Directory:
    def __init__(self, name):
        self.name = name  # Directory name
        self.subdirectories = {}  # Dictionary to hold subdirectories

    def add_subdirectory(self, path_parts):
        """Add a subdirectory at the specified path."""
        if not path_parts:
            return
        part = path_parts[0]
        if part not in self.subdirectories:
            self.subdirectories[part] = Directory(part)
        self.subdirectories[part].add_subdirectory(path_parts[1:])

    def move_subdirectory(self, src, dest):
        """Move a subdirectory from src to dest."""
        if src in self.subdirectories:
            self.subdirectories[dest] = self.subdirectories.pop(src)

    def delete_subdirectory(self, path_parts):
        """Delete a subdirectory at the specified path."""
        if len(path_parts) == 1:
            if path_parts[0] in self.subdirectories:
                del self.subdirectories[path_parts[0]]
                return True
            else:
                return False
        else:
            next_part = path_parts[0]
            if next_part in self.subdirectories:
                return self.subdirectories[next_part].delete_subdirectory(path_parts[1:])
            else:
                return False

    def list_structure(self):
        """List the current directory structure using an iterative approach."""
        stack = [(self, 0)]  # Stack for DFS traversal
        while stack:
            current, level = stack.pop()
            indent = '  ' * level
            print(f"{indent}{current.name}")
            for subdir in sorted(current.subdirectories.values(), key=lambda x: x.name, reverse=True):
                stack.append((subdir, level + 1))

    def find_subdirectory(self, path_parts):
        """Find a subdirectory at the specified path."""
        if not path_parts:
            return self
        part = path_parts[0]
        if part in self.subdirectories:
            return self.subdirectories[part].find_subdirectory(path_parts[1:])
        else:
            return None


class DirectoryTree:
    def __init__(self):
        self.root = Directory('')  # Initialize with a root directory

    def create(self, path):
        """Create a new directory at the specified path."""
        path_parts = path.split('/')
        self.root.add_subdirectory(path_parts)
        print(f"CREATE {path}")

    def move(self, src, dest):
        """Move a directory from src to dest."""
        src_parts = src.split('/')
        dest_parts = dest.split('/')

        src_dir = self.root.find_subdirectory(src_parts[:-1])
        dest_dir = self.root.find_subdirectory(dest_parts)

        if src_dir and dest_dir and src_parts[-1] in src_dir.subdirectories:
            src_dir.move_subdirectory(src_parts[-1], src_parts[-1])
            dest_dir.subdirectories[src_parts[-1]] = src_dir.subdirectories[src_parts[-1]]
            print(f"MOVE {src} {dest}")
        else:
            print(f"Cannot move {src} to {dest} - Invalid path(s)")

    def delete(self, path):
        """Delete a directory at the specified path."""
        path_parts = path.split('/')
        if not self.root.delete_subdirectory(path_parts):
            print(f"Cannot delete {path} - Directory not found")
        else:
            print(f"DELETE {path}")

    def list_tree(self):
        """List the current directory structure."""
        print("LIST")
        self.root.list_structure()


class CommandParser:
    def __init__(self):
        self.tree = DirectoryTree()

    def parse_and_execute(self, command):
        """Parse and execute a given command."""
        parts = command.split()
        action = parts[0]

        if action == "CREATE" and len(parts) == 2:
            self.tree.create(parts[1])
        elif action == "MOVE" and len(parts) == 3:
            self.tree.move(parts[1], parts[2])
        elif action == "DELETE" and len(parts) == 2:
            self.tree.delete(parts[1])
        elif action == "LIST" and len(parts) == 1:
            self.tree.list_tree()
        else:
            print(f"Invalid command: {command}")


def main():
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

    parser = CommandParser()

    for command in commands:
        parser.parse_and_execute(command)


# Unit tests for DirectoryTree
def test_directory_tree():
    tree = DirectoryTree()

    # Test creating directories
    tree.create('test')
    tree.create('test/folder1')
    tree.create('test/folder1/subfolder')
    assert 'folder1' in tree.root.subdirectories['test'].subdirectories

    # Test moving directories
    tree.create('newtest')
    tree.move('test/folder1', 'newtest')
    assert 'folder1' in tree.root.subdirectories['newtest'].subdirectories

    # Test deleting directories
    tree.delete('newtest/folder1')
    assert 'folder1' not in tree.root.subdirectories['newtest'].subdirectories

    print("All unit tests passed!")


if __name__ == "__main__":
    main()
    test_directory_tree()
