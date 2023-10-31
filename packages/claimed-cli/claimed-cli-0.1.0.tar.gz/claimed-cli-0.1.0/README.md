# cli
CLAIMED CLI - all components available via cli at your fingertips

## Installation

```bash
pip install claimed-cli
```

## Example usage
Run an operator locally:
```bash
claimed claimed-util-cos:0.3 access_key_id="xxx" secret_access_key="yyy" endpoint="https://s3.us-east.cloud-object-storage.appdomain.cloud" bucket_name="era5-cropscape-zarr" path="/" recursive=True operation=ls
```

Create operators using [C3](https://github.com/claimed-framework/c3):
```bash
claimed create operator <file> -r <repository>
```

