import sys
sys.path.append('.')
from app.ml_model.summarizer import get_model
model = get_model()
text = "India, located in South Asia, is the seventh largest country in the world and the second most populous country, home to more than 1.4 billion people. Its rich culture, diversity, and historical significance make it a unique country. India has an area of 32,87,263 square kilometers, extending from the heights of the Himalayas to tropical rain forests. India's democratic government, prosperous economy, and cultural heritage include unique traditions, languages, festivals and arts."
print("SUMMARY:", model.summarize(text, max_length=200, min_length=50))
