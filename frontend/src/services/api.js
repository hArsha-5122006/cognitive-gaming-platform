const API_BASE_URL = 'http://localhost:8000';

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
  async getPatientId(token) {
    const res = await fetch(`${API_BASE_URL}/api/auth/me/patient`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Failed to fetch patient id');
    const data = await res.json();
    return data.id;
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
  },
  async getAnalytics(token, patientId) {
    const res = await fetch(`${API_BASE_URL}/api/performance/analytics/${patientId}`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Failed to fetch analytics');
    return res.json();
  },
  async getCaregiverDashboard(token) {
    const res = await fetch(`${API_BASE_URL}/api/caregivers/dashboard`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Failed to fetch dashboard');
    return res.json();
  },
  async getCaregiverAlerts(token, patientId) {
    const res = await fetch(`${API_BASE_URL}/api/caregivers/alerts/${patientId}`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) throw new Error('Failed to fetch alerts');
    return res.json();
  },
  savePendingResult(resultData) {
    let pending = JSON.parse(localStorage.getItem('pendingGameResults') || '[]');
    pending.push(resultData);
    localStorage.setItem('pendingGameResults', JSON.stringify(pending));
  },
  getPendingResults() {
    return JSON.parse(localStorage.getItem('pendingGameResults') || '[]');
  },
  clearPendingResults() {
    localStorage.removeItem('pendingGameResults');
  },
  async syncPendingResults(token) {
    const pending = this.getPendingResults();
    if (pending.length === 0) return;
    const failed = [];
    for (const result of pending) {
      try {
        await this.submitGameResult(token, result);
      } catch (err) {
        console.error('Sync failed for result, keeping in pending:', err);
        failed.push(result);
      }
    }
    localStorage.setItem('pendingGameResults', JSON.stringify(failed));
  },
  cacheReminders(reminders) {
    localStorage.setItem('cachedReminders', JSON.stringify(reminders));
  },
  getCachedReminders() {
    return JSON.parse(localStorage.getItem('cachedReminders') || '[]');
  }
};
