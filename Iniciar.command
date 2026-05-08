#!/bin/bash
cd "/Users/noriol/Proyectos/Humanity Last Exam"
.venv/bin/streamlit run src/app.py &
sleep 2 && open http://localhost:8503
wait
