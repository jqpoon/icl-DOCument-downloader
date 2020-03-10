# icl-cate-downloader
A simple python script to help download coursework specifications and answers.

## Getting Started

### Prerequisites
`python 3.7`
- `beautifulsoup4 4.8.2`
- `Requests 2.22.0`

### Usage
1. Download script with wget or curl

```wget link_here```

2. Edit file with your username and password, set output directory

3. Run script with python

```python main.py```

This writes to the output directory specified, with the following structure

```
output_dir
│
└───(course #) - (course_name)
│   │
│   └───exercises
│       │   (#)_(TUT|CW|PMT) - (name).pdf
│       │   1_CW - Coursework 1.pdf
│       │   ...
│   
└───113 - Introduction to Computer Architecture
|
...
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
