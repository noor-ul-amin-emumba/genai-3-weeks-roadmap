# Current Approach Limitations

1. **Chunking Strategy Issue**: The current chunking strategy may be inadequate. The resume clearly indicates three previous employers, but the RAG system identifies only two (Emumba and Productbox). Improving the chunking strategy is necessary to capture all employment history accurately.

2. **Date Awareness Issue**: The system lacks current date awareness. When queried about professional experience and duration, it returns "**Emumba Private Limited (Full Stack Developer)**: 08/05/2023 - CURRENT (approx. 1 year)" instead of calculating the actual 2 years and 9 months based on today's date. The RAG system must be integrated with current date and time information.
