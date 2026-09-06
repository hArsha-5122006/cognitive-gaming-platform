import { useState } from 'react';
import { api } from '../services/api';

function Login({ onLogin, onSwitchToSignup }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const data = await api.login(email, password);
      localStorage.setItem('token', data.access_token);
      onLogin(data.access_token);
    } catch (err) {
      setError('Login failed. Please check your email and password.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-blue-50">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
        <h1 className="text-4xl font-bold text-center text-blue-800 mb-6">Welcome</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-4 text-2xl border-2 border-gray-300 rounded-xl focus:outline-none focus:border-blue-500"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-4 text-2xl border-2 border-gray-300 rounded-xl focus:outline-none focus:border-blue-500"
            required
          />
          {error && <p className="text-red-600 text-xl">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white text-2xl font-bold py-4 rounded-xl disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        <p className="text-center mt-4">
          Don't have an account? <button onClick={onSwitchToSignup} className="text-blue-600">Sign Up</button>
        </p>
      </div>
    </div>
  );
}

export default Login;
