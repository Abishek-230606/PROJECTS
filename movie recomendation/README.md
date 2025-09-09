# 🎬 Movie Recommendation System (Content-Based)

This project implements a **Content-Based Movie Recommendation System** using metadata such as genres, keywords, cast, crew, and overview.  
It suggests the top-5 most similar movies for a given movie title using **TF-IDF vectorization** and **cosine similarity**.

---

## 📌 Features
- Uses **movie metadata**: genres, keywords, overview, top 3 cast, and director.  
- **TF-IDF vectorization** with n-grams for text representation.  
- **Cosine similarity** to measure closeness between movies.  
- Fuzzy title matching (handles typos in movie names).  
- Returns top-5 recommendations with similarity scores.  

---

## ⚙️ Workflow
1. **Load Dataset**  
   Dataset: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)  
   Keep only required columns: `movie_id, title, genres, keywords, overview, cast, crew`.

2. **Preprocessing**  
   - Parse JSON-like fields (`genres`, `keywords`, `cast`, `crew`).  
   - Keep only top 3 cast members and director.  
   - Clean text (remove spaces in tokens, handle missing values).  

3. **Feature Engineering**  
   - Create a combined text column from genres, keywords, cast, crew, and overview.  
   - Apply weighting → genres ×3, keywords ×2.  

4. **Vectorization & Similarity**  
   - Use **TF-IDF** to convert text into numeric vectors.  
   - Compute **cosine similarity matrix** between all movies.  

5. **Recommendation Function**  
   - Input: Movie title (with fuzzy matching).  
   - Output: Top-5 most similar movies with similarity scores.  

---

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/movie-recommender.git
   cd movie-recommender
   ```

2. Install dependencies:
   ```bash
   pip install pandas scikit-learn
   ```

3. Run Jupyter Notebook:
   ```bash
   jupyter notebook movie_recommender.ipynb
   ```

4. Try recommendations:
   ```python
   recommend("Inception", top=5)
   recommend("Interstellar", top=5)
   recommend("Iron Man", top=5)
   ```

---

## 📊 Example Output
```text
Recommendations for 'Inception':
[('Interstellar', 0.431), ('Shutter Island', 0.398), ('The Prestige', 0.376), ('Memento', 0.355), ('The Matrix', 0.342)]
```

---

## 📉 Limitations
- Pure content-based (does not learn from user ratings).  
- Quality depends on metadata completeness.  
- Does not capture deeper semantic meaning (can be improved with embeddings).  

---

## 🔮 Future Improvements
- Use **sentence embeddings** for semantic similarity.  
- Add **collaborative filtering** with user ratings.  
- Build a **Streamlit/Flask UI** for interactive demos.  
- Evaluate with metrics like **precision@k**.  

---

## 👨‍💻 Author
- Project by Abishek JS  
- Built as part of a Machine Learning task (2nd Year, CSE AI/ML)

