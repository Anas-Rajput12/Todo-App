'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { isAuthenticated } from '../lib/auth';
import Header from '../../components/Header';


/* =========================
   MAIN PAGE COMPONENT
========================= */
export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated()) {
      router.push('/dashboard');
    }
  }, [router]);

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-indigo-50 via-white to-purple-50 overflow-x-hidden">
      <Header />

      {/* ================= HERO SECTION ================= */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-16 sm:pt-32 sm:pb-24">

        <section className="text-center">
          <h1
            className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold
            bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600
            bg-clip-text text-transparent"
          >
            Streamline Your Tasks
            <span className="block">Amplify Productivity</span>
          </h1>

          <p className="mt-6 max-w-2xl mx-auto text-gray-600 text-base sm:text-lg md:text-xl">
            A modern task management platform designed to help you organize,
            focus, and achieve more with clarity and speed.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row justify-center gap-4">
            <Link
  href="/signup"
  className="
    w-full sm:w-auto
    inline-flex items-center justify-center
    gap-3
    px-8 py-4
    rounded-xl
    bg-indigo-600 text-white font-semibold
    shadow-lg
    transition-all
    hover:bg-indigo-700 hover:scale-105
  "
>
  <span className="text-center">Start Free Trial</span>

  <svg
    className="h-6 w-6"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 20 20"
    fill="currentColor"
    aria-hidden="true"
  >
    <path
      fillRule="evenodd"
      d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
      clipRule="evenodd"
    />
  </svg>
</Link>


            <Link
              href="/login"
              className="px-8 py-4 rounded-xl border-2 border-indigo-300
              text-indigo-600 font-semibold hover:bg-indigo-50 hover:scale-105 transition-all"
            >
              Sign In to Dashboard
            </Link>
          </div>
        </section>

        {/* ================= FEATURES SECTION ================= */}
        <section className="mt-28">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
              Why Choose TaskFlow?
            </h2>
            <p className="mt-4 text-gray-600 max-w-xl mx-auto">
              Everything you need to stay productive, focused, and ahead.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Feature
              title="Organize Effortlessly"
              text="Create, prioritize, and manage tasks with a clean and intuitive workflow."
            />
            <Feature
              title="Track Progress"
              text="Visual insights help you understand progress and improve performance."
            />
            <Feature
              title="Achieve Goals"
              text="Smart reminders and focus tools help you reach goals faster."
            />
          </div>
        </section>

        {/* ================= STATS SECTION ================= */}
        <section
          className="mt-32 rounded-3xl bg-gradient-to-r from-indigo-600 to-purple-600
          p-10 text-white text-center"
        >
          <h2 className="text-3xl sm:text-4xl font-bold mb-6">
            Trusted by Productive People
          </h2>

          <p className="text-indigo-100 max-w-xl mx-auto mb-10">
            Thousands of users rely on TaskFlow every day.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
            <Stat value="98%" label="Boosted Productivity" />
            <Stat value="2.5x" label="Faster Completion" />
            <Stat value="50k+" label="Active Users" />
          </div>
        </section>

        {/* ================= FINAL CTA ================= */}
        <section className="mt-32 text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
            Ready to Take Control?
          </h2>
          <p className="text-gray-600 max-w-xl mx-auto mb-8">
            Start organizing your tasks today — fast, simple, and free.
          </p>

          <Link
            href="/signup"
            className="inline-block px-10 py-4 rounded-2xl
            bg-gradient-to-r from-indigo-600 to-purple-600
            text-white font-semibold shadow-xl
            hover:scale-105 transition-all"
          >
            Create Free Account
          </Link>
        </section>
      </main>

      {/* ================= FOOTER ================= */}
      <footer className="mt-32 border-t bg-white/80 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 py-8 text-center">
          <p className="text-gray-500 text-sm">
            © {new Date().getFullYear()} TaskFlow. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}

/* =========================
   HELPER COMPONENTS
========================= */

function Stat({ value, label }: { value: string; label: string }) {
  return (
    <div>
      <div className="text-4xl font-bold mb-2">{value}</div>
      <div className="text-indigo-200">{label}</div>
    </div>
  );
}

function Feature({ title, text }: { title: string; text: string }) {
  return (
    <div
      className="bg-white rounded-3xl p-8 shadow-lg
      hover:-translate-y-2 hover:shadow-2xl transition-all"
    >
      <h3 className="text-xl font-bold text-gray-900 mb-3 text-center">
        {title}
      </h3>
      <p className="text-gray-600 text-center">{text}</p>
    </div>
  );
}
