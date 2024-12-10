import mimetypes


def chunks_indexes_by_number_of_chunks(length, n_chunks):
    max_chunk_length = length // n_chunks + (length % n_chunks > 0)
    return chunks_indexes_by_max_len_of_chunk(length, max_chunk_length)


def chunks_indexes_by_max_len_of_chunk(length, max_chunk_length):
    indexes = []
    for i in range(0, length, max_chunk_length):
        indexes.append(list(range(i, min(i + max_chunk_length, length))))
    return indexes


def is_text_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is not None and mime_type.startswith("text")
