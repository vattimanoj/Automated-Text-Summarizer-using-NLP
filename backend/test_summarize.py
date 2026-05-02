
from app.ml_model.summarizer import SummarizationModel
import logging
import sys

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def test_summarization():
    print("Initializing SummarizationModel...")
    model = SummarizationModel()
    
    test_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. 
    AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.
    The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving".
    This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.
    AI applications include advanced web search engines (e.g., Google Search), recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), generative or creative tools (ChatGPT and AI art), and competing at the highest level in strategic game systems (such as chess and Go).
    """
    
    print("\nOriginal Text Length:", len(test_text))
    print("\nGenerating summary...")
    
    try:
        summary = model.summarize(test_text, max_length=150, min_length=30)
        print("\nSummary:")
        print(summary)
        print("\nSummary Length:", len(summary))
    except Exception as e:
        print(f"\nError during summarization: {e}")

if __name__ == "__main__":
    test_summarization()
