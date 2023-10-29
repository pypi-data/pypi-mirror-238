import zlib
import os


def extract_file_based_on_header_info(apk_file, local_header_info, central_directory_info):
    """
    Extracts a single file from the apk_file based on the information provided from the offset and the header_info.
    It takes into account that the compression method provided might not be STORED or DEFLATED and in that case
    it attempts to inflate it (Android < 9) and if that fails it considers it as STORED (Android >= 9).
    :param apk_file: The already read/loaded data of the APK file e.g. with open('test.apk', 'rb') as apk_file
    :param local_header_info: The local header dictionary info for that specific filename (parse_local_header)
    :param central_directory_info:
    :return: Returns the actual extracted data for that file
    """
    filename_length = local_header_info["file_name_length"]
    if local_header_info["compressed_size"] == 0 or local_header_info["uncompressed_size"] == 0:
        compressed_size = central_directory_info["compressed_size"]
        uncompressed_size = central_directory_info["uncompressed_size"]
    else:
        compressed_size = local_header_info["compressed_size"]
        uncompressed_size = local_header_info["uncompressed_size"]

    extra_field_length = local_header_info["extra_field_length"]
    compression_method = local_header_info["compression_method"]
    # Skip the offset + local header to reach the compressed data
    local_header_size = 30  # Size of the local header in bytes
    offset = central_directory_info["relative_offset_of_local_file_header"]
    apk_file.seek(offset + local_header_size + filename_length + extra_field_length)
    if compression_method == 0:  # Stored (no compression)
        compressed_data = apk_file.read(compressed_size)
        extracted_data = compressed_data
        indicator = 'STORED'
    elif compression_method == 8:
        compressed_data = apk_file.read(compressed_size)
        # -15 for windows size due to raw stream with no header or trailer
        extracted_data = zlib.decompress(compressed_data, -15)
        indicator = 'DEFLATED'
    else:
        try:
            cur_loc = apk_file.tell()
            compressed_data = apk_file.read(compressed_size)
            extracted_data = zlib.decompress(compressed_data, -15)
            indicator = 'DEFLATED_TAMPERED'
        except:
            apk_file.seek(cur_loc)
            compressed_data = apk_file.read(uncompressed_size)
            extracted_data = compressed_data
            indicator = 'STORED_TAMPERED'
    return extracted_data, indicator


def extract_all_files_from_central_directory(apk_file, central_directory_entries, local_header_entries, output_dir):
    """
    Extracts all files from an APK based on the entries detected in the central_directory_entries.
    :param apk_file: The already read/loaded data of the APK file e.g. with open('test.apk', 'rb') as apk_file
    :param central_directory_entries: The dictionary with all the entries for the central directory
    :param local_header_entries: The dictionary with all the local header entries
    :param output_dir: The output directory where to save the files.
    :return: Returns 0 if no errors, 1 if an exception and 2 if the output directory already exists
    """
    try:
        # Check if the output directory already exists
        if os.path.exists(output_dir):
            print("Extraction aborted. Output directory already exists.")
            return 2
        # Create the output directory or overwrite if it already exists
        os.makedirs(output_dir, exist_ok=True)
        # Iterate over central directory entries
        for filename, cd_header_info in central_directory_entries.items():
            # Extract the file using the local header information
            extracted_data = extract_file_based_on_header_info(apk_file, local_header_entries[filename], cd_header_info)[0]
            # Construct the output file path
            output_path = os.path.join(output_dir, filename)
            # Create directories if necessary
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            # Write the extracted data to the output file
            with open(output_path, 'wb') as output_file:
                output_file.write(extracted_data)
        return 0
    except Exception as e:
        print(f"Error extracting files: {e}")
        return 1
