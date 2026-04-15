#!/bin/bash
cd "/Users/noriol/Google Drive - Mi Unidad/noriol/Abedul 3/NOH/VS Code Projects/Humanity Last Exam"
.venv/bin/streamlit run src/app.py &
sleep 2 && open http://localhost:8503
wait
