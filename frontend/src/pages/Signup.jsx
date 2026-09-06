import { useState } from 'react';

function Signup({ onSignupSuccess }) {
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState('patient');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await fetch('http://localhost:8000/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, full_name: fullName, role, password }),
      });
      if (!res.ok) throw new Error('Signup failed');
      onSignupSuccess();
    } catch (err) {
      setError('Signup failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-blue-50">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
        <h1 className="text-4xl font-bold text-center text-blue-800 mb-6">Sign Up</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-4 text-2xl border-2 rounded-xl"
            required
          />
          <input
            type="text"
            placeholder="Full Name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            className="w-full p-4 text-2xl border-2 rounded-xl"
            required
          />
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="w-full p-4 text-2xl border-2 rounded-xl"
          >
            <option value="patient">Patient</option>
            <option value="caregiver">Caregiver</option>
          </select>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-4 text-2xl border-2 rounded-xl"
            required
          />
          {error && <p className="text-red-600 text-xl">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white text-2xl font-bold py-4 rounded-xl"
          >
            {loading ? 'Signing up...' : 'Sign Up'}
          </button>
        </form>
        <p className="text-center mt-4">
          Already have an account? <button onClick={onSignupSuccess} className="text-blue-600">Login</button>
        </p>
      </div>
    </div>
  );
}

export default Signup;
