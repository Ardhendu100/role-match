Embeddings are used to convert text into vector representations that can be stored in a vector database and used for similarity search.
Embedding = Meaning in numbers.
Two similar texts will have similar vectors.
Example:
"Python backend developer"


"Backend engineer using Python"


These will produce vectors that are close in vector space.
Later we will measure that closeness using:
cosine similarity


That is how job matching works.

---------------------------------------------------------

🧠 First: Why Do We Need Cosine Similarity?

When we create embeddings, we convert text into vectors:

"Python backend developer"
→ [0.21, -0.88, 0.43, ...]  (384 numbers)

Now the question is:

👉 How do we measure if two vectors mean similar things?

We need a similarity function.

That function is:

Cosine similarity


🎯 What Cosine Similarity Measures

It measures:

The angle between two vectors.

Not the distance.
Not the magnitude.
Only the angle.

Why angle?

Because magnitude (vector length) doesn’t represent meaning.
Direction represents meaning.

Think of vectors like arrows in space.

If two arrows point in:

Same direction → Very similar → cosine ≈ 1

90° angle → Unrelated → cosine ≈ 0

Opposite direction → Opposite meaning → cosine ≈ -1

So result range is:

-1  → completely opposite
 0  → unrelated
+1  → identical meaning


In embeddings, usually:

0.7+ → very similar

0.4 → somewhat related

0.1 → unrelated

🎯 Why This Matters

This is EXACTLY how job matching works.

In our case:

Resume embedding
↓
Compare against job embeddings
↓
Sort by similarity
↓
Top 5 matches

That’s the core engine.

----------------------------------------------------

🧠 Think Like an Engineer (Not Just a Rule Follower)

Cosine similarity range:

-1   → opposite meaning
 0   → unrelated
+1   → identical meaning


So:

0.85 → strong alignment

0.42 → moderate alignment

0.05 → almost unrelated

We choose the highest score because:

Higher cosine similarity = smaller angle between vectors = more semantic similarity.

---------------------------------------------------

🔥 Now Big Realization

Your job matching system is basically:

For each job:
    score = cosine(resume, job)

Sort by score descending
Return top 5


That’s it.

No magic.
No AI thinking.
Just vector math.

The LLM comes later to explain.

----------------------------------


🧠 This Is Very Important

Embeddings are not truth.

They are:

The model’s learned representation of meaning.

So if two unrelated texts get 0.92 similarity, it means:

The model thinks they are similar

The training data shaped that understanding

The vector space structure caused them to align

It does NOT mean objective truth.


🔥 This Is Why Model Choice Matters

Different embedding models produce:

Different vector spaces

Different similarity behavior

Different matching quality

That’s why in real companies:

Model evaluation is important

You test retrieval quality

You tune thresholds


🧠 Now You Are Thinking Like an AI Engineer

You just understood:

Matching = math

Meaning = learned representation

High similarity = model alignment, not absolute truth

This is foundational knowledge for:

RAG systems

Vector databases

AI search engines


---------------------------

🧠 First Question

How are those numeric vectors created?

When you do:

model.encode("Python backend developer")


Internally this happens:

1️⃣ Text → Tokenization
2️⃣ Tokens → Numbers
3️⃣ Numbers → Neural Network
4️⃣ Neural Network → 384-dimensional vector

Let’s unpack that.


Step 1 — Tokenization

The sentence:

"Python backend developer"


Gets split into tokens like:

["Python", "backend", "developer"]


Actually internally it becomes token IDs like:

[7592, 18723, 10234]


Each word becomes an integer.


Step 2 — Word Embeddings (Initial Layer)

Each token ID is mapped to a learned vector.

Example (simplified):

Python → [0.21, -0.55, 0.90, ...]
backend → [0.11, -0.22, 0.44, ...]

These are learned during training on massive datasets.


Step 3 — Transformer Layers

The model (MiniLM, which is based on BERT architecture) passes those vectors through multiple transformer layers.

Inside each layer:

Attention mechanism

Matrix multiplications

Nonlinear transformations

Context mixing

After many layers, the model produces a final contextual representation.

That final representation becomes your 384-length embedding.



🎯 Now Your Main Question

How can two unrelated texts get 0.92 similarity?

There are a few possibilities.

1️⃣ The Model Sees Hidden Similarity

Example:

Text A:

"I work with neural networks"


Text B:

"I build AI systems"


You may think different.
Model thinks related.

So similarity high.

2️⃣ Dataset Bias

The model learned relationships from its training data.

If two concepts frequently appeared together in training,
their vectors may become aligned.

3️⃣ Embedding Space Compression

Remember:

We compress meaning into only 384 numbers.

That is a HUGE compression.

Language is infinitely complex.
Model must approximate.

So sometimes:
Two unrelated texts may accidentally land in nearby space.

This is called:

False positive in semantic similarity.


4️⃣ Limited Model Capacity

MiniLM is small.

Smaller models:

Faster

Cheaper

But less precise

Bigger models usually produce cleaner embedding spaces.

-------------------------------------------------------------------

🔥 Deep Engineering Truth

Vector similarity is:

Approximate semantic similarity.

Not perfect.
Not logical.
Not reasoning-based.

It is learned geometry.