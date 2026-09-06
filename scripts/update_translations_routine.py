from pathlib import Path

# We'll read the current file, add keys, and write back
path = Path("frontend/src/services/translations.js")
content = path.read_text(encoding='utf-8')

# Add opening_routine key to both language objects
# English
content = content.replace(
    "opening_progress: 'Opening progress.',",
    "opening_progress: 'Opening progress.',\n    opening_routine: 'Opening daily routine.',"
)
# Telugu
content = content.replace(
    "opening_progress: 'పురోగతిని తెరుస్తున్నాను.',",
    "opening_progress: 'పురోగతిని తెరుస్తున్నాను.',\n    opening_routine: 'దినచర్య తెరుస్తున్నాను.',"
)
path.write_text(content, encoding='utf-8')
print("translations.js updated with routine keys!")
