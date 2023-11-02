
# setup docker env
```text
docker build -t utils_cv -f docker/Dockerfile .
docker run -it --rm --name utils_cv -v .\:/code utils_cv bash
```


This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

Change Logs
- v0.0.10
    - add utils_dataset
- v0.0.11
    - get_area return 0 if box invalid