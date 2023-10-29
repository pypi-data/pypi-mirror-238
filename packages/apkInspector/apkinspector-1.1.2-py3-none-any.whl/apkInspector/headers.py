import struct
from typing import Dict
from .helpers import pretty_print_header, save_to_json


class EndOfCentralDirectoryRecord:
    def __init__(self, signature, number_of_this_disk, disk_where_central_directory_starts,
                 number_of_central_directory_records_on_this_disk,
                 total_number_of_central_directory_records, size_of_central_directory,
                 offset_of_start_of_central_directory, comment_length, comment):
        self.signature = signature
        self.number_of_this_disk = number_of_this_disk
        self.disk_where_central_directory_starts = disk_where_central_directory_starts
        self.number_of_central_directory_records_on_this_disk = number_of_central_directory_records_on_this_disk
        self.total_number_of_central_directory_records = total_number_of_central_directory_records
        self.size_of_central_directory = size_of_central_directory
        self.offset_of_start_of_central_directory = offset_of_start_of_central_directory
        self.comment_length = comment_length
        self.comment = comment

    @classmethod
    def parse(cls, apk_file):
        """
        Method to locate the "end of central directory record signature" as the first step of the correct process of
        reading a ZIP archive. Should be noted that certain APKs do not follow the zip specification and declare multiple
        "end of central directory records". For this reason the search for the corresponding signature of the eocd starts
        from the end of the apk.
        :param apk_file: The already read/loaded data of the APK file e.g. with open('test.apk', 'rb') as apk_file
        :return: Returns the end of central directory record with all the information available if the corresponding
        signature is found. If not, then it returns None.
        """
        chunk_size = 1024
        offset = 0
        signature_offset = -1
        file_size = apk_file.seek(0, 2)
        while offset < file_size:
            position = file_size - offset - chunk_size
            if position < 0:
                position = 0
            apk_file.seek(position)
            chunk = apk_file.read(chunk_size)
            if not chunk:
                break
            signature_offset = chunk.rfind(b'\x50\x4b\x05\x06')  # end of Central Directory File Header signature
            if signature_offset != -1:
                eo_central_directory_offset = position + signature_offset
                break  # Found End of central directory record (EOCD) signature
            offset += chunk_size
        if signature_offset == -1:
            raise ValueError("End of central directory record (EOCD) signature not found")
        apk_file.seek(eo_central_directory_offset)

        signature = apk_file.read(4)
        number_of_this_disk = struct.unpack('<H', apk_file.read(2))[0]
        disk_where_central_directory_starts = struct.unpack('<H', apk_file.read(2))[0]
        number_of_central_directory_records_on_this_disk = struct.unpack('<H', apk_file.read(2))[0]
        total_number_of_central_directory_records = struct.unpack('<H', apk_file.read(2))[0]
        size_of_central_directory = struct.unpack('<I', apk_file.read(4))[0]
        offset_of_start_of_central_directory = struct.unpack('<I', apk_file.read(4))[0]
        comment_length = struct.unpack('<H', apk_file.read(2))[0]
        comment = struct.unpack(f'<{comment_length}s', apk_file.read(comment_length))[0].decode('utf-8')
        return cls(
            signature,
            number_of_this_disk,
            disk_where_central_directory_starts,
            number_of_central_directory_records_on_this_disk,
            total_number_of_central_directory_records,
            size_of_central_directory,
            offset_of_start_of_central_directory,
            comment_length,
            comment
        )

    def to_dict(self):
        return {
            "signature": self.signature,
            "number_of_this_disk": self.number_of_this_disk,
            "disk_where_central_directory_starts": self.disk_where_central_directory_starts,
            "number_of_central_directory_records_on_this_disk": self.number_of_central_directory_records_on_this_disk,
            "total_number_of_central_directory_records": self.total_number_of_central_directory_records,
            "size_of_central_directory": self.size_of_central_directory,
            "offset_of_start_of_central_directory": self.offset_of_start_of_central_directory,
            "comment_length": self.comment_length,
            "comment": self.comment
        }

    @classmethod
    def from_dict(cls, entry_dict):
        return cls(**entry_dict)


class CentralDirectoryEntry:
    def __init__(self, version_made_by, version_needed_to_extract, general_purpose_bit_flag,
                 compression_method, file_last_modification_time, file_last_modification_date,
                 crc32_of_uncompressed_data, compressed_size, uncompressed_size, file_name_length,
                 extra_field_length, file_comment_length, disk_number_where_file_starts,
                 internal_file_attributes, external_file_attributes, relative_offset_of_local_file_header,
                 filename, extra_field, file_comment, offset_in_central_directory):
        self.version_made_by = version_made_by
        self.version_needed_to_extract = version_needed_to_extract
        self.general_purpose_bit_flag = general_purpose_bit_flag
        self.compression_method = compression_method
        self.file_last_modification_time = file_last_modification_time
        self.file_last_modification_date = file_last_modification_date
        self.crc32_of_uncompressed_data = crc32_of_uncompressed_data
        self.compressed_size = compressed_size
        self.uncompressed_size = uncompressed_size
        self.file_name_length = file_name_length
        self.extra_field_length = extra_field_length
        self.file_comment_length = file_comment_length
        self.disk_number_where_file_starts = disk_number_where_file_starts
        self.internal_file_attributes = internal_file_attributes
        self.external_file_attributes = external_file_attributes
        self.relative_offset_of_local_file_header = relative_offset_of_local_file_header
        self.filename = filename
        self.extra_field = extra_field
        self.file_comment = file_comment
        self.offset_in_central_directory = offset_in_central_directory

    def to_dict(self):
        return {
            "version_made_by": self.version_made_by,
            "version_needed_to_extract": self.version_needed_to_extract,
            "general_purpose_bit_flag": self.general_purpose_bit_flag,
            "compression_method": self.compression_method,
            "file_last_modification_time": self.file_last_modification_time,
            "file_last_modification_date": self.file_last_modification_date,
            "crc32_of_uncompressed_data": self.crc32_of_uncompressed_data,
            "compressed_size": self.compressed_size,
            "uncompressed_size": self.uncompressed_size,
            "file_name_length": self.file_name_length,
            "extra_field_length": self.extra_field_length,
            "file_comment_length": self.file_comment_length,
            "disk_number_where_file_starts": self.disk_number_where_file_starts,
            "internal_file_attributes": self.internal_file_attributes,
            "external_file_attributes": self.external_file_attributes,
            "relative_offset_of_local_file_header": self.relative_offset_of_local_file_header,
            "filename": self.filename,
            "extra_field": self.extra_field,
            "file_comment": self.file_comment,
            "offset_in_central_directory": self.offset_in_central_directory
        }

    @classmethod
    def from_dict(cls, entry_dict):
        return cls(**entry_dict)


class CentralDirectory:
    def __init__(self, entries):
        self.entries = entries

    @classmethod
    def parse(cls, apk_file, eocd: EndOfCentralDirectoryRecord = None):
        """
        Method that is used to parse the central directory header according to the specification
        https://pkware.cachefly.net/webdocs/APPNOTE/APPNOTE-6.3.9.TXT
        based on the offset provided by the end of central directory record: eocd["Offset of start of central directory"].
        If multiple central directory headers are discovered this will not be handled properly!

        :param apk_file: The already read/loaded data of the APK file e.g. with open('test.apk', 'rb') as apk_file
        :param eocd: End of central directory record
        :return: Returns a dictionary with all the entries discovered. The filename of each entry is used as the key. Besides
        the fields defined by the specification, each entry has an additional field named 'Offset in the central directory header',
        which includes the offset of the entry in the central directory itself.
        """
        if not eocd:
            eocd = EndOfCentralDirectoryRecord.parse(apk_file)
        apk_file.seek(eocd.offset_of_start_of_central_directory)
        if apk_file.tell() != eocd.offset_of_start_of_central_directory:
            raise ValueError(f"Failed to find the offset for the central directory within the file!")

        central_directory_entries = {}
        while True:
            c_offset = apk_file.tell()
            signature = apk_file.read(4)
            if signature != b'\x50\x4b\x01\x02':
                break  # Reached the end of the central directory
            version_made_by = struct.unpack('<H', apk_file.read(2))[0]
            version_needed_to_extract = struct.unpack('<H', apk_file.read(2))[0]
            general_purpose_bit_flag = struct.unpack('<H', apk_file.read(2))[0]
            compression_method = struct.unpack('<H', apk_file.read(2))[0]
            file_last_modification_time = struct.unpack('<H', apk_file.read(2))[0]
            file_last_modification_date = struct.unpack('<H', apk_file.read(2))[0]
            crc32_of_uncompressed_data = struct.unpack('<I', apk_file.read(4))[0]
            compressed_size = struct.unpack('<I', apk_file.read(4))[0]
            uncompressed_size = struct.unpack('<I', apk_file.read(4))[0]
            file_name_length = struct.unpack('<H', apk_file.read(2))[0]
            extra_field_length = struct.unpack('<H', apk_file.read(2))[0]
            file_comment_length = struct.unpack('<H', apk_file.read(2))[0]
            disk_number_where_file_starts = struct.unpack('<H', apk_file.read(2))[0]
            internal_file_attributes = struct.unpack('<H', apk_file.read(2))[0]
            external_file_attributes = struct.unpack('<I', apk_file.read(4))[0]
            relative_offset_of_local_file_header = struct.unpack('<I', apk_file.read(4))[0]
            filename = struct.unpack(f'<{file_name_length}s', apk_file.read(file_name_length))[0].decode('utf-8')
            extra_field = struct.unpack(f'<{extra_field_length}s', apk_file.read(extra_field_length))[0].decode('utf-8',
                                                                                                                'ignore')
            file_comment = struct.unpack(f'<{file_comment_length}s', apk_file.read(file_comment_length))[0].decode(
                'utf-8', 'ignore')
            offset_in_central_directory = c_offset

            central_directory_entry = CentralDirectoryEntry(
                version_made_by, version_needed_to_extract, general_purpose_bit_flag, compression_method,
                file_last_modification_time, file_last_modification_date, crc32_of_uncompressed_data,
                compressed_size, uncompressed_size, file_name_length, extra_field_length, file_comment_length,
                disk_number_where_file_starts, internal_file_attributes, external_file_attributes,
                relative_offset_of_local_file_header, filename, extra_field, file_comment,
                offset_in_central_directory
            )
            central_directory_entries[central_directory_entry.filename] = central_directory_entry

        return cls(central_directory_entries)

    def to_dict(self):
        return {filename: entry.to_dict() for filename, entry in self.entries.items()}

    @classmethod
    def from_dict(cls, entry_dict):
        return cls(**entry_dict)


class LocalHeaderRecord:
    def __init__(self, version_needed_to_extract, general_purpose_bit_flag,
                 compression_method, file_last_modification_time, file_last_modification_date,
                 crc32_of_uncompressed_data, compressed_size, uncompressed_size, file_name_length,
                 extra_field_length, filename, extra_field):

        self.version_needed_to_extract = version_needed_to_extract
        self.general_purpose_bit_flag = general_purpose_bit_flag
        self.compression_method = compression_method
        self.file_last_modification_time = file_last_modification_time
        self.file_last_modification_date = file_last_modification_date
        self.crc32_of_uncompressed_data = crc32_of_uncompressed_data
        self.compressed_size = compressed_size
        self.uncompressed_size = uncompressed_size
        self.file_name_length = file_name_length
        self.extra_field_length = extra_field_length
        self.filename = filename
        self.extra_field = extra_field

    @classmethod
    def parse(cls, apk_file, entry_of_interest: CentralDirectoryEntry):
        """
        Method that attempts to read the local file header according to the specification
        https://pkware.cachefly.net/webdocs/APPNOTE/APPNOTE-6.3.9.TXT

        :param apk_file: The already read/loaded data of the APK file e.g. with open('test.apk', 'rb') as apk_file
        :param entry_of_interest: The central directory header of the specific entry of interest
        :return: Returns a dictionary with the local header information or None if it failed to find the header.
        """
        apk_file.seek(entry_of_interest.relative_offset_of_local_file_header)
        header_signature = apk_file.read(4)

        if not header_signature == b'\x50\x4b\x03\x04':
            print(f"Does not seem to be the start of a local header!")
            return None
        else:
            version_needed_to_extract = struct.unpack('<H', apk_file.read(2))[0]
            general_purpose_bit_flag = struct.unpack('<H', apk_file.read(2))[0]
            compression_method = struct.unpack('<H', apk_file.read(2))[0]
            file_last_modification_time = struct.unpack('<H', apk_file.read(2))[0]
            file_last_modification_date = struct.unpack('<H', apk_file.read(2))[0]
            crc32_of_uncompressed_data = struct.unpack('<I', apk_file.read(4))[0]
            compressed_size = struct.unpack('<I', apk_file.read(4))[0]
            uncompressed_size = struct.unpack('<I', apk_file.read(4))[0]
            file_name_length = struct.unpack('<H', apk_file.read(2))[0]
            extra_field_length = struct.unpack('<H', apk_file.read(2))[0]
            filename = struct.unpack(f'<{file_name_length}s', apk_file.read(file_name_length))[0].decode('utf-8')
            extra_field = struct.unpack(f'<{extra_field_length}s', apk_file.read(extra_field_length))[0].decode('utf-8',
                                                                                                                'ignore')
        return cls(
            version_needed_to_extract, general_purpose_bit_flag, compression_method,
            file_last_modification_time, file_last_modification_date, crc32_of_uncompressed_data,
            compressed_size, uncompressed_size, file_name_length, extra_field_length,
            filename, extra_field)

    def to_dict(self):
        return {
            "version_needed_to_extract": self.version_needed_to_extract,
            "general_purpose_bit_flag": self.general_purpose_bit_flag,
            "compression_method": self.compression_method,
            "file_last_modification_time": self.file_last_modification_time,
            "file_last_modification_date": self.file_last_modification_date,
            "crc32_of_uncompressed_data": self.crc32_of_uncompressed_data,
            "compressed_size": self.compressed_size,
            "uncompressed_size": self.uncompressed_size,
            "file_name_length": self.file_name_length,
            "extra_field_length": self.extra_field_length,
            "filename": self.filename,
            "extra_field": self.extra_field
        }

    @classmethod
    def from_dict(cls, entry_dict):
        return cls(**entry_dict)


class ZipEntry:
    def __init__(self, eocd: EndOfCentralDirectoryRecord, central_directory: CentralDirectory, local_headers: Dict[str, LocalHeaderRecord]):
        self.eocd = eocd
        self.central_directory = central_directory
        self.local_headers = local_headers

    @classmethod
    def parse(cls, apk_file):
        eocd = EndOfCentralDirectoryRecord.parse(apk_file)
        central_directory = CentralDirectory.parse(apk_file, eocd)
        local_headers = {}
        for entry in central_directory.entries:
            local_header_entry = LocalHeaderRecord.parse(apk_file, central_directory.entries[entry])
            local_headers[local_header_entry.filename] = local_header_entry
        return cls(eocd, central_directory, local_headers)

    @classmethod
    def parse_single(cls, apk_file, filename, eocd: EndOfCentralDirectoryRecord = None, central_directory: CentralDirectory = None):
        if not eocd or not central_directory:
            eocd = EndOfCentralDirectoryRecord.parse(apk_file)
            central_directory = CentralDirectory.parse(apk_file, eocd)
        local_header = {filename: LocalHeaderRecord.parse(apk_file, central_directory.entries[filename])}
        return cls(eocd, central_directory, local_header)

    def to_dict(self):
        return {
            "end_of_central_directory": self.eocd.to_dict(),
            "central_directory": self.central_directory.to_dict(),
            "local_headers": {filename: entry.to_dict() for filename, entry in self.local_headers.items()}
        }

    def get_central_directory_entry_dict(self, filename):
        if filename in self.central_directory.entries:
            return self.central_directory.entries[filename].to_dict()
        else:
            return None

    def get_local_header_dict(self, filename):
        if filename in self.local_headers:
            return self.local_headers[filename].to_dict()
        else:
            return None


def print_headers_of_filename(cd_h_of_file, local_header_of_file):
    """
    Prints out the details for both the central directory header and the local file header. Useful for the CLI
    :param cd_h_of_file: central directory header of a filename as it may be retrieved from headers_of_filename
    :param local_header_of_file: local header dictionary of a filename as it may be retrieved from headers_of_filename
    """
    if not cd_h_of_file or not local_header_of_file:
        print("Are you sure the filename exists?")
        return
    pretty_print_header("CENTRAL DIRECTORY")
    for k in cd_h_of_file:
        if k == 'Relative offset of local file header' or k == 'Offset in the central directory header':
            print(f"{k:40} : {hex(int(cd_h_of_file[k]))} | {cd_h_of_file[k]}")
        else:
            print(f"{k:40} : {cd_h_of_file[k]}")
    pretty_print_header("LOCAL HEADER")
    for k in local_header_of_file:
        print(f"{k:40} : {local_header_of_file[k]}")


def show_and_save_info_of_headers(entries, apk_name, header_type: str, export: bool, show: bool):
    """
    Print information for each entry for the central directory header and allow to possibly export to JSON
    :param entries: The dictionary with all the entries for the central directory (see parse_central_directory)
    :param apk_name: String with the name of the APK, so it can be used for the export.
    :param header_type: What type of header that is, either central_directory or local
    :param export: Boolean for exporting or not to JSON
    :param show: Boolean for printing or not the entries
    """
    if show:
        for entry in entries:
            pretty_print_header(entry)
            print(entries[entry])
    if export:
        save_to_json(f"{apk_name}_{header_type}_header.json", entries)

