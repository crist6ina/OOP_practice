"""Interview question - ReadEquipment class, allows the reading and processing
of network equipment data"""
import os.path
import pandas as pd


class ReadEquipment:
    """ReadEquipment class
    Objects of this class may be created based on a .txt file containing
    specific network equipment data."""

    def __init__(self, file: str):
        """ReadEquipment constructor"""
        self.file = file
        self.network_element_name = ReadEquipment.readfile(self).split()[1]

    def readfile(self) -> str:
        """Return txt file content in a string."""
        if os.path.exists(self.file):
            with open(self.file, 'r') as fr:
                content = fr.read()
                return content
        else:
            raise FileNotFoundError

    def __split_content(self, row: int = None) -> list[list[str]] or str:
        """Return a list of lists, where each list represents a row and has each word as a
        separate element. If a specific row was specified, the row as a string will be returned"""
        row_list = self.readfile().split('\n')
        if row:
            return row_list[row]
        word_list = [row.split() for row in row_list if row.split()]
        return word_list

    @property
    def result_of_operation(self) -> str:
        """Checks if operation was successful and returns said result."""
        content = self.__split_content()[3]
        return ' '.join(content[-2::])

    def file_content_to_dataframe(self):
        """Creates dataframe object from given file where the columns are represented by
        Local Cell ID(index), Cell Name, Column_2, Column_3 specific to network element."""
        # actual columns as lists
        config_list = self.__split_content()[7:-2]

        # list with header names
        raw_df_header = self.__split_content(7).split('  ')
        df_header = [header.strip() for header in raw_df_header if header.strip()]

        # creating dataframe
        info_dataframe = pd.DataFrame(config_list, columns=df_header)
        info_dataframe = info_dataframe.set_index('Local Cell ID')
        return info_dataframe

    def get_column_by_name(self, column: str, local_cell_id: str = '') -> str:
        """Return entire column of dataframe by giving column name as argument.
        A specific row of the column may be returned if local_cell_id index is provided."""
        info_dataframe = self.file_content_to_dataframe()
        if local_cell_id:
            if local_cell_id not in info_dataframe[column]:
                raise ValueError('Invalid Local Cell ID.')
            return f'{column}: id {local_cell_id} -> {info_dataframe[column][local_cell_id]}'
        return info_dataframe[column]

    def __str__(self):
        return (f'ReadEquipment object [{self.network_element_name}] '
                f'with status: {self.result_of_operation}')


if __name__ == '__main__':
    try:
        eq = ReadEquipment('network_element_data.txt')
        print(eq.network_element_name)
        print(eq.result_of_operation)
        data = eq.file_content_to_dataframe()
        print(data)
        column_3 = eq.get_column_by_name('Column_3', '2')
        print(column_3)
    except FileNotFoundError:
        print('File not found.')
    except ValueError as e:
        print(e)
