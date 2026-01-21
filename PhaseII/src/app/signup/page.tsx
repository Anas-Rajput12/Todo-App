'use client';

import Link from 'next/link';
import SignupForm from '../../components/auth/SignupForm';

export default function SignupPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="text-center mb-10">
          <div className="mx-auto flex items-center justify-center">
            <div className="h-14 w-14 rounded-2xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center shadow-lg">
              <svg className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
              </svg>
            </div>
          </div>
          <h1 className="mt-6 text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">Create Account</h1>
          <p className="mt-3 text-sm text-gray-500">Join us today and start organizing your tasks efficiently</p>
        </div>

        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white p-8 transition-all duration-500 hover:shadow-2xl">
          <SignupForm />
        </div>

        <div className="mt-8 text-center text-sm text-gray-500">
          <p>
            Already have an account?{' '}
            <a href="/login" className="font-bold text-indigo-600 hover:text-purple-600 transition-all duration-300 transform hover:scale-105 hover:underline">
              Sign in
            </a>
          </p>
        </div>

        <div className="mt-10 text-center text-xs text-gray-400">
          <p>Secure & encrypted registration</p>
        </div>
      </div>
    </div>
  );
}