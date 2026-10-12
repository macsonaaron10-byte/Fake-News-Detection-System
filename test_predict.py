from predict import predict_news

headline = """
Breaking: Government announces
new healthcare initiative.
"""

result = predict_news(headline)

print("Prediction:", result["prediction"])
print("Confidence:", result["confidence"])