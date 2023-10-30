
# windows
```text
docker build -t ocr_data_generator -f docker/Dockerfile .
docker run -it --rm --name ocr_data_generator -v .\:/code ocr_data_generator bash

```