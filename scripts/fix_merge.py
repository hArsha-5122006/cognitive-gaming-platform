from pathlib import Path

path = Path("ai/models/train_model.py")
content = path.read_text(encoding='utf-8')
old = """    if not results.empty:
        reaction_agg = results.groupby('session_id')['reaction_time_ms'].mean().reset_index()
        reaction_agg.columns = ['session_id', 'avg_reaction_time_ms']
        sessions = sessions.merge(reaction_agg, on='session_id', how='left')
        sessions['avg_reaction_time_ms'] = sessions['avg_reaction_time_ms'].fillna(0)
    else:
        sessions['avg_reaction_time_ms'] = 0"""
new = """    if not results.empty:
        reaction_agg = results.groupby('session_id')['reaction_time_ms'].mean().reset_index()
        reaction_agg.columns = ['session_id', 'avg_reaction_time_ms']
        # Sessions table has 'id' as session identifier
        sessions = sessions.merge(reaction_agg, left_on='id', right_on='session_id', how='left')
        sessions['avg_reaction_time_ms'] = sessions['avg_reaction_time_ms'].fillna(0)
    else:
        sessions['avg_reaction_time_ms'] = 0"""
content = content.replace(old, new)
path.write_text(content, encoding='utf-8')
print("Fixed merge in train_model.py")
