## Tripadvisor Hotel Image Downloader

Using this you should be able to download hotel images from tripadvisor. 

To get started make sure you have **Google Chrome** and then install the requirements.txt

```python
pip install -r requirements.txt
```

Open the _**main.py**_ file and make edits as needed. You might be using the script multiple times for this reason I title argument _**super\_download\_folder\_title**_. Think of it as your project name. Then there is a dictionary _**search\_dict**_. You can use the search dict to execute multiple searches in in one project. 

For example, you might want to scrape images based on hotel names, continents, countries, etc. The downloader will iterate over the dictionary and will download images for one key: value pair at a time. 

The intermediary URLs are saved in the folder. The final folder structure is as follows:

```python
downloads
- super_download_folder_title
  - search_dict[key1]
    - list_item 1
    - list_item 2
  - search_dict[key2]
    - list_item 1
    - list_item 2
```

An example could be

```python
downloads
- Continents
  - Europe
    - England
      - 0_1.jpg
      - 0_2.jpg
  - Asia
    - India
      - 0_1.jpg
      - 0_2.jpg
    - China
      - 0_1.jpg
      - 0_2.jpg
  - Continent
    - Europe
      - 0_1.jpg
      - 0_2.jpg
```

Simply edit the _**main.py**_ file as per your requirements and run it from the terminal using

```python
python main.py
```
