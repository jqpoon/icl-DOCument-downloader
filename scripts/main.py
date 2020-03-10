from bs4 import BeautifulSoup
import requests
import re
import os


########################### DEFINITIONS ###########################

dry_run = False # False to see if what would have ran

my_auth = ("username", r"password")
spring_homepage = "link_to_spring_homepage"

base_link = "https://cate.doc.ic.ac.uk/"
base_path = "/path/to/your/directory"

module_dict = {"Introduction to Computer Architecture": "113 - ",
               "Programming II (Java)": "120.2 - ",
               "Introduction to Databases": "130 - ",
               "Reasoning about Programs": "141 - ",
               "Graphs and Algorithms": "150 - ",
               "Computing Practical 1": "161 - ",
               "Professional Issues": "166 - "}

def href_is_file(href):
    return href and re.compile("^showfile").search(href)

def href_is_answer(href):
    return href and re.compile("^showfile.*MODELS.*").search(href)

def href_is_data(href):
    return href and re.compile("^showfile.*DATA.*").search(href)

########################### FILE HANDLING ###########################

def download_file(name, url, output_path):
    """Downloads file at url to
    output path using requests"""
    if not (dry_run or os.path.isfile(output_path)):
        create_dir_if_not_exist(os.path.dirname(output_path))

        response = requests.get(url, auth=my_auth)
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print("Successfully downloaded: " + name)
    else:
        print("Dry run or file already exists, not downloading file: " + name)

def create_dir_if_not_exist(dir_path):
    if not dry_run:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    else:
        print("Dry run, not creating dir: " + dir_path)

########################### GET NAMES ###########################

def get_file_name(item):
    file_name = item.contents[0].strip()
    file_prefix = item.find_previous_sibling().contents[0]
    file_name = file_prefix + " - " + file_name
    return file_name.replace(':', '_')

def get_module_name(item):
    sibling = item.find_next_sibling()
    while (sibling["href"].find("mailto") == -1):
        sibling = sibling.find_next_sibling()
    module_name = re.compile(r"(.*)'(.*)'(.*)").search(sibling["href"]).group(2)
    return module_name

def get_given_href(item):
    given = item.find_next_sibling()

    if not given:
        return (False, "")
    if not given["href"].startswith("given"):
        return (False, "")
    else:
        return (True, given["href"])

########################### MAIN ###########################

def simple_soup(link):
    html_response = requests.get(link, auth=my_auth).text
    return BeautifulSoup(html_response, features='html.parser')

def get_given_link(link):
    html_response = requests.get(link, auth=my_auth).content
    ans_soup = BeautifulSoup(html_response, features='html.parser')
    ans_dl_href = ans_soup.find('a', href=href_is_answer)
    data_dl_href = ans_soup.find('a', href=href_is_data)

    if ans_dl_href:
        return ("ans", ans_dl_href["href"])
    elif data_dl_href:
        return ("data", data_dl_href["href"])
    else:
        print("Error: no valid href found on external page: " + link)

def main():
    soup_object = simple_soup(spring_homepage)
    for item in soup_object.find_all('a', href=href_is_file):
        module_name = get_module_name(item)
        download_dir = base_path + module_dict[module_name] + module_name + "/exercises/"

        spec_name =  get_file_name(item)
        spec_dl_link = base_link + item["href"]
        spec_dl_path = download_dir + spec_name + ".pdf"

        (has_ext, ext_href_link) = get_given_href(item)
        if has_ext:
            (ext_type, ext_dl_link) = get_given_link(base_link + ext_href_link)
            ext_dl_link = base_link + ext_dl_link

            if ext_type == "ans":
                ext_dl_path = download_dir + spec_name + "_ANS" + ".pdf"
                download_file(spec_name + "_ANS", ext_dl_link, ext_dl_path)
            elif ext_type == "data":
                ext_dl_path = download_dir + spec_name + "_DATA"
                download_file(spec_name + "_DATA", ext_dl_link, ext_dl_path)

        ##### DOWNLOAD FILES ######
        download_file(spec_name, spec_dl_link, spec_dl_path)



if __name__ == '__main__':
    main()
    print("Done!")
