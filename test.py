with open("urls.txt", 'r') as urls_file:
    all_urls = urls_file.readlines()
    for each_url in all_urls:
        print(each_url.strip().rstrip('\n'))