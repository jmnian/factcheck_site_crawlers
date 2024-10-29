import pickle 

with open("crawlers/rfa/rfa_all_article_boxes.pkl", "rb") as file:
    search_results = pickle.load(file)

print(len(search_results))