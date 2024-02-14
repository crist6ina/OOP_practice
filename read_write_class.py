"""FileWriter and FileReader classes"""
import sys
import os
from pathlib import Path


class FileTypeError:
    pass


class FileExtensionError:
    pass


class AccessFile:
    def __init__(self, filename: str):
        """AccessFile constructor"""
        self.filename = filename
        if not isinstance(self.filename, str):
            raise FileTypeError
        self.parent_path = str(Path(__file__).parent)
        self.path = self.parent_path + '/' + self.filename
        self.parent = self.parent_path[self.parent_path.rindex('/') + 1::]

    @property
    def size(self):
        """Return file size"""
        try:
            return os.path.getsize(self.filename)
        except FileNotFoundError:
            print(f'Cannot get size because {self.filename} was not found')
            sys.exit(2)


class FileDeleter(AccessFile):
    """FileDeleter class"""

    def __init__(self, filename):
        """FileDeleter constructor"""
        super().__init__(filename)

    def delete_file(self):
        """Delete file from directory if it exists."""
        if os.path.exists(self.path):
            press = input(f'This action will completely remove {self.filename}. Do you want to proceed?(yes/no) ')
            if press == 'yes':
                os.remove(self.path)
            else:
                sys.exit(0)
        else:
            print(f'{self.filename} does not exist in {self.parent}')


class FileWriter(AccessFile):
    """FileWriter class"""
    def __init__(self, filename: str):
        """FileWriter constructor"""
        super().__init__(filename)

    def _write_to_file(self, data: str, mode='a'):
        """Write data to file"""
        if not isinstance(data, str):
            raise ValueError('Content must be of str type')

        with open(self.filename, mode) as fw:
            fw.write(f'{data}\n')

    def writer(self, content: str, mode='a'):
        """Write or append data to file"""
        if not isinstance(content, str):
            raise ValueError

        if os.path.exists(self.path) and mode == 'w':
            press = input(f'{self.filename} is an existing file in {self.parent} directory. '
                          f'Are you sure you want to overwrite?(yes/append/no) ')
            if press == 'yes':
                self._write_to_file(content, 'w')
            elif press == 'append':
                self._write_to_file(content, 'a')
            else:
                sys.exit(0)
        elif not os.path.exists(self.path) and mode == 'a':
            print(f'{self.filename} does not exist in {self.parent} directory. New file will be created.')
            self._write_to_file(content)
        else:
            self._write_to_file(content)

    @classmethod
    def from_file(cls, file: str) -> list:
        """Alternative constructor"""
        if not os.path.exists(file):
            raise FileNotFoundError(f'The file does not exist')
        file_objects = []
        with open(file, 'r') as fr:
            content = fr.readlines()

        for file_name in content:
            file_objects.append(cls(file_name.strip()))
        return file_objects

    def __str__(self):
        return self.filename


class FileReader(FileWriter):
    """FileReader class"""
    def __init__(self, filename: str):
        """FileReader constructor"""
        super().__init__(filename)

    def reader(self):
        """Return content of given file"""
        try:
            with open(self.path, 'r') as fread:
                content = fread.read()
                return content
        except FileNotFoundError:
            sys.exit('File not found')


if __name__ == '__main__':
    # tester_file = input('Choose file to manipulate: ')
    # tester = ManipulateFile(tester_file)
    try:
        text_file = FileWriter('dummy2.txt')
        text_file.writer('nu')
        reader_objects = FileReader.from_file('files.txt')
        object_list = [obj.filename for obj in reader_objects]
        print(text_file)
        print(object_list)
    except ValueError:
        print('Value error!')
