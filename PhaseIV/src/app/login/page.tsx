'use client';

import Link from 'next/link';
import LoginForm from '../../components/auth/LoginForm';

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="text-center mb-10">
          <div className="mx-auto flex items-center justify-center">
            <div className="h-14 w-14 rounded-2xl bg-gradient-to-br from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg">
              <svg className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
            </div>
          </div>
          <h1 className="mt-6 text-3xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Welcome Back</h1>
          <p className="mt-3 text-sm text-gray-500">Sign in to your account to continue your productivity journey</p>
        </div>

        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white p-8 transition-all duration-500 hover:shadow-2xl">
          <LoginForm />
        </div>

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>
            Don't have an account?{' '}
            <a href="/signup" className="font-bold text-indigo-600 hover:text-purple-600 transition-all duration-300 transform hover:scale-105 hover:underline">
              Sign up now
            </a>
          </p>
        </div>

        <div className="mt-10 text-center text-xs text-gray-400">
          <p>Secure & encrypted authentication</p>
        </div>
      </div>
    </div>
  );
}