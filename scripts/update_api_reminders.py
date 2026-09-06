from pathlib import Path

content = '''const API_BASE_URL = 'http://localhost:8000';

export const api = {
  async login(email, password) {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    const res = await fetch(`${API_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: formData,
    });
    if (!res.ok) throw new Error('Login failed');
    return res.json();
  },
  async getMe(token) {
    const res = await fetch(`${API_BASE_URL}/api/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Not authenticated');
    return res.json();
  },
  async submitGameResult(token, resultData) {
    const res = await fetch(`${API_BASE_URL}/api/games/submit_result`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(resultData),
    });
    if (!res.ok) throw new Error('Failed to submit result');
    return res.json();
  },
  async getReminders(token) {
    const res = await fetch(`${API_BASE_URL}/api/reminders/`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Failed to fetch reminders');
    return res.json();
  },
  async completeReminder(token, reminderId) {
    const res = await fetch(`${API_BASE_URL}/api/reminders/${reminderId}/complete`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Failed to complete reminder');
    return res.json();
  }
};
'''

path = Path("frontend/src/services/api.js")
path.write_text(content.strip(), encoding='utf-8')
print("api.js updated with reminder methods!")
