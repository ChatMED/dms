# MinIO Storage Service User Guide

This script demonstrates how to interact with a MinIO storage service. It includes functionality for managing buckets, uploading and downloading files, setting bucket policies, and handling error scenarios gracefully using Python and the MinIO Python SDK.

## Features

- **Bucket Management**
  - Create a bucket if it doesn’t already exist.
  - Delete an empty bucket.
  - Force delete a non-empty bucket, including all its objects and versions.

- **File Management**
  - List files in a bucket.
  - Upload files to a bucket.
  - Delete files from a bucket.

- **Bucket Policy Management**
  - Get the current bucket policy.
  - Set a new bucket policy.

- **Logging**
  - Logs all activities to `minio_access.log` and the console.

---

## Requirements

1. **Python Version**: Python 3.7 or higher
2. **Dependencies**:
   - `minio`: Install using `pip install minio`

---

## Configuration

The script reads MinIO configuration from a JSON file named `minio_config.json`. The file should contain the following fields:

```json
{
  "endpoint": "YOUR_MINIO_ENDPOINT",
  "access_key": "YOUR_ACCESS_KEY",
  "secret_key": "YOUR_SECRET_KEY"
}
```
## Setup

1. **Install Dependencies**:
   First, install the required dependencies:
   ```bash
   pip install minio
   ```
2. **Prepare Configuration File**: Create minio_config.json with your MinIO credentials and endpoint.

3. **Prepare a File for Testing**: Ensure you have a file named example.txt in the script's directory to upload to the MinIO bucket.

## Usage

### Main Script Workflow

The `main()` function demonstrates the following operations:

1. **Logging Setup**: Configures logging to both console and a file (`minio_access.log`).
2. **Load Configuration**: Reads credentials and endpoint from `minio_config.json`.
3. **Connect to MinIO**: Establishes a connection to the MinIO server.

#### Bucket Operations:
- Creates a bucket named `example-bucket` if it doesn’t exist.
- Uploads `example.txt` to the bucket.
- Lists files in the bucket.
- Applies a bucket policy to allow public access.
- Retrieves and logs the current bucket policy.
- Deletes the uploaded file.
- Deletes the bucket (both normal and forced deletion are demonstrated).

### Key Functions

#### 1. **Bucket Operations**
- `create_bucket(client, bucket_name)`: Creates a new bucket.
- `delete_bucket(client, bucket_name)`: Deletes an empty bucket.
- `force_delete_bucket(client, bucket_name)`: Deletes a bucket and all its contents.

#### 2. **File Operations**
- `upload_file(client, bucket_name, file_path, object_name)`: Uploads a file to a bucket.
- `list_files(client, bucket_name)`: Lists all files in a bucket.
- `delete_object_from_bucket(client, bucket_name, object_name)`: Deletes a specific file from a bucket.

#### 3. **Bucket Policy**
- `get_bucket_policy(client, bucket_name)`: Fetches and logs the current bucket policy.
- `set_bucket_policy(client, bucket_name, policy)`: Sets a new policy for the bucket.

### Example Run

1. Run the script:

   ```bash
   python script.py
   ```

2. Check `minio_access.log` for detailed logs of all operations.


## Error Handling

The script uses robust error handling to:

- Log and raise exceptions for critical errors (e.g., connection issues, missing configuration).
- Warn about non-critical issues (e.g., versioned objects missing during forced deletion).

---

## Logging

- **File Logs**: Stored in `minio_access.log` with timestamps and log levels.
- **Console Logs**: Mirrors file logs for real-time monitoring.

---

## Extending the Script

You can extend the script to:

- Handle object versioning in more detail.
- Add support for downloading files.
- Include advanced bucket lifecycle policies.

---

## References

- [MinIO Python SDK Documentation](https://docs.min.io/docs/python-client-quickstart-guide.html)

