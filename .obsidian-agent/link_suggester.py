#!/usr/bin/env python3
import os
import re
import math
import argparse
from organizer import ObsidianNote, VaultOrganizer

# Stopwords for English and Korean to improve similarity results
STOPWORDS = {
    # English
    'the', 'and', 'of', 'to', 'a', 'in', 'that', 'is', 'was', 'for', 'on', 'it', 'as', 'with', 'by', 'an', 'be', 'this',
    'are', 'from', 'at', 'i', 'you', 'he', 'she', 'they', 'we', 'or', 'but', 'not', 'your', 'my', 'their', 'our', 'will',
    # Korean
    '은', '는', '이', '가', '을', '를', '에', '의', '와', '과', '으로', '로', '하다', '이다', '있다', '없다', '그리고', '하지만',
    '그래서', '그러나', '하지만', '또한', '에서', '에게', '한테', '부터', '까지', '하고', '하며', '등', '등등', '것', '수', '한',
    '할', '하고', '한다', '했다', '입니다', '합니다', '으로', '로써', '로시', '적', '의해', '위해', '대한', '대해', '통해'
}

def tokenize(text):
    """Tokenize text into lowercased alphanumeric words, preserving Korean and English."""
    # Matches words containing Korean syllables, English letters, and numbers
    words = re.findall(r'[a-zA-Z가-힣0-9]+', text.lower())
    # Filter stopwords and short terms (length < 2, except for crucial short Korean concepts)
    filtered = []
    for w in words:
        if w not in STOPWORDS and len(w) >= 2:
            filtered.append(w)
    return filtered

class SimilarityEngine:
    def __init__(self, notes):
        self.notes = notes # title -> ObsidianNote
        self.documents = {} # title -> tokens list
        self.vocab = set()
        self.idf = {}
        
    def build_index(self):
        # Tokenize all note bodies
        for title, note in self.notes.items():
            # Combine title (weighted higher) and body content
            combined_text = (title + " ") * 3 + note.body_content
            tokens = tokenize(combined_text)
            self.documents[title] = tokens
            for token in tokens:
                self.vocab.add(token)
                
        # Calculate IDF
        num_docs = len(self.documents)
        if num_docs == 0:
            return
            
        doc_frequencies = {token: 0 for token in self.vocab}
        for tokens in self.documents.values():
            unique_tokens = set(tokens)
            for token in unique_tokens:
                doc_frequencies[token] += 1
                
        for token, df in doc_frequencies.items():
            # Standard IDF formula with smoothing
            self.idf[token] = math.log((1 + num_docs) / (1 + df)) + 1

    def get_tf_vector(self, tokens):
        """Calculate TF-IDF vector for a list of tokens."""
        tf = {}
        for token in tokens:
            tf[token] = tf.get(token, 0) + 1
            
        vector = {}
        for token, count in tf.items():
            if token in self.idf:
                vector[token] = count * self.idf[token]
        return vector

    def cosine_similarity(self, vec1, vec2):
        """Calculate Cosine Similarity between two sparse vectors."""
        intersection = set(vec1.keys()).intersection(set(vec2.keys()))
        if not intersection:
            return 0.0
            
        dot_product = sum(vec1[token] * vec2[token] for token in intersection)
        
        magnitude1 = math.sqrt(sum(val**2 for val in vec1.values()))
        magnitude2 = math.sqrt(sum(val**2 for val in vec2.values()))
        
        if magnitude1 == 0.0 or magnitude2 == 0.0:
            return 0.0
            
        return dot_product / (magnitude1 * magnitude2)

    def suggest_connections(self, threshold=0.10, limit=5):
        """Scans vault and lists recommended links."""
        self.build_index()
        suggestions = []
        
        titles = list(self.notes.keys())
        num_titles = len(titles)
        
        # Calculate TF-IDF vectors for all notes
        vectors = {}
        for title in titles:
            vectors[title] = self.get_tf_vector(self.documents[title])
            
        # Pairwise comparison
        for i in range(num_titles):
            title_a = titles[i]
            note_a = self.notes[title_a]
            vec_a = vectors[title_a]
            
            for j in range(i + 1, num_titles):
                title_b = titles[j]
                note_b = self.notes[title_b]
                vec_b = vectors[title_b]
                
                # Skip if already linked in either direction
                if title_b in note_a.links or title_a in note_b.links:
                    continue
                    
                score = self.cosine_similarity(vec_a, vec_b)
                if score >= threshold:
                    # Find common matching terms to show why they are linked
                    matching_terms = sorted(
                        list(set(vec_a.keys()).intersection(set(vec_b.keys()))),
                        key=lambda x: vec_a[x] * vec_b[x],
                        reverse=True
                    )[:3]
                    
                    suggestions.append({
                        "note_a": title_a,
                        "note_b": title_b,
                        "score": score,
                        "terms": matching_terms
                    })
                    
        # Sort by similarity score descending
        suggestions.sort(key=lambda x: x["score"], reverse=True)
        return suggestions

def main():
    parser = argparse.ArgumentParser(description="Obsidian Organic Link Suggester")
    parser.add_argument("--vault", type=str, default="..", help="Path to your Obsidian Vault (defaults to parent directory)")
    parser.add_argument("--threshold", type=float, default=0.10, help="Similarity threshold for link recommendation (default: 0.10)")
    
    args = parser.parse_args()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vault_path = args.vault
    if vault_path == "..":
        vault_path = os.path.dirname(script_dir)
        
    organizer = VaultOrganizer(vault_path)
    organizer.scan_vault()
    
    if len(organizer.notes) < 2:
        print("⚠ Too few notes to compute similarities.")
        return
        
    print("\n🧠 Analyzing text similarities and discovering organic connections...")
    engine = SimilarityEngine(organizer.notes)
    suggestions = engine.suggest_connections(threshold=args.threshold)
    
    recommendations_file = os.path.join(script_dir, "link_recommendations.md")
    
    with open(recommendations_file, 'w', encoding='utf-8') as f:
        f.write("# 🔮 Organic Link Recommendations\n\n")
        f.write(f"Analyzed **{len(organizer.notes)}** notes with a similarity threshold of **{args.threshold:.2f}**.\n")
        f.write(f"Found **{len(suggestions)}** potential organic connections that aren't currently linked.\n\n")
        
        if not suggestions:
            f.write("✔ No unlinked highly-similar notes found! Your notes are already extremely well-connected.\n")
            print("✔ No unlinked notes met the similarity threshold.")
        else:
            f.write("| Note A | Note B | Similarity Score | Shared Core Concepts |\n")
            f.write("| :--- | :--- | :---: | :--- |\n")
            for sug in suggestions[:50]: # Top 50 suggestions
                note_a = sug["note_a"]
                note_b = sug["note_b"]
                score = sug["score"]
                terms = ", ".join([f"`{t}`" for t in sug["terms"]])
                f.write(f"| [[{note_a}]] | [[{note_b}]] | **{score:.3f}** | {terms} |\n")
                
            print(f"✔ Organic link suggestions computed. Top {min(10, len(suggestions))} recommendations:")
            for sug in suggestions[:10]:
                print(f"  • [[{sug['note_a']}]] ⟷ [[{sug['note_b']}]] (Score: {sug['score']:.3f}, Key: {', '.join(sug['terms'])})")
                
            print(f"\n📂 Full list written to: `.obsidian-agent/link_recommendations.md`")

if __name__ == "__main__":
    main()
