import spacy

def detect_voice_distribution(text):
	nlp = spacy.load("en_core_web_sm")
	doc = nlp(text)

	active_count = 0
	passive_count = 0

	for sent in doc.sents:
		is_passive = False
		for token in sent:
			# Check for auxiliary verbs that often indicate passive voice
			if token.dep_ == "auxpass" or (token.dep_ == "aux" and token.head.tag_ == "VBN"):
				is_passive = True
				break

		if is_passive:
			passive_count += 1
			print(sent)
		else:
			active_count += 1

	total_sentences = active_count + passive_count
	active_percentage = (active_count / total_sentences) * 100 if total_sentences else 0
	passive_percentage = (passive_count / total_sentences) * 100 if total_sentences else 0

	return {
		"total_sentences": total_sentences,
		"active_count": active_count,
		"passive_count": passive_count,
		"active_percentage": active_percentage,
		"passive_percentage": passive_percentage,
	}


# Example usage
if __name__ == "__main__":
	text = """To increase the accessibility of this powerful model class and at the same time reduce its significant resource consumption, a method is needed that reduces the computational complexity for both training and sampling. Reducing the computational demands of DMs without impairing their performance is, therefore, key to enhance their accessibility.

Departure to Latent Space Our approach starts with the analysis of already trained diffusion models in pixel space: Fig. 2 shows the rate-distortion trade-off of a trained model. As with any likelihood-based model, learning can be roughly divided into two stages: First is a perceptual compression stage which removes high-frequency details but still learns little semantic variation. In the second stage, the actual generative model learns the semantic and conceptual composition of the data (semantic compression)."""

	result = detect_voice_distribution(text)
	print("Total Sentences:", result["total_sentences"])
	print("Active Sentences:", result["active_count"])
	print("Passive Sentences:", result["passive_count"])
	print("Active Voice Percentage: {:.2f}%".format(result["active_percentage"]))
	print("Passive Voice Percentage: {:.2f}%".format(result["passive_percentage"]))
