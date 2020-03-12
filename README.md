# icl-DOCument-downloader
A simple python script to help download coursework specifications and answers.

## Getting Started

### Prerequisites
`python 3.7`
- `beautifulsoup4 4.8.2`
- `Requests 2.22.0`

### Usage
1. Download script with wget or curl. Alternatively, simply navigate to link and download script.

```
wget https://raw.githubusercontent.com/jqpoon/icl-DOCument-downloader/master/scripts/main.py
```

2. Edit file with your username and password, set output directory

3. Run script with python

```
python main.py
```

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

## Future plans
- Add option to use password files instead of raw passwods
- Add config file to read from
- Download course notes as well
- Expand to download from materials.doc.ic.ac.uk

## License
[MIT](https://choosealicense.com/licenses/mit/)
