# https://github.com/jcontini/google-keep-csv
# keep notes extracted using Google Takeout

# this processes the json files to get the first nntation description

#!/usr/bin/env python
# coding: utf-8
import os, json, glob, csv
import datetime
os.system('cls' if os.name == 'nt' else 'clear')

files = glob.glob("Keep/**/*.json",recursive=True)
if 'Keep/archive_browser.html' in files: files.remove('Keep/archive_browser.html')

# Prep CSV file
now = datetime.datetime.now()
csvout = "notes_%s.csv" % now.strftime("%Y-%m-%d_%H%M")

with open(csvout, "w", encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerow(["file", "date", "title", "content", "category"])

    for file in files:
        print(file)
        try:
            with open(file, mode="r", encoding='utf8') as page:
                j = json.load(page)

            timestamp_microseconds = j["userEditedTimestampUsec"]
            timestamp_seconds = timestamp_microseconds/1000000
            dobj = datetime.datetime.fromtimestamp(timestamp_seconds)
            xlDate = dobj.isoformat()
            title = j["title"]
            url = j["textContent"]
            content = j["annotations"][0]["description"] + \
                " <a href='" + url + "'>" + url + '</a>'

            note = {"date": xlDate, "title": title, "content": content} # , "description": desc}
            # , note["description"]
            writer.writerow(
                [file, note["date"], note["title"], note["content"], "keep"])
        except:
            print("** error in file " + file)

print("\n" + "-" * 50 + "\nDone! %s notes saved to %s\n" % (len(files), csvout))
