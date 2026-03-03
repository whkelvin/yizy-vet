import { redirect, type Handle } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import { ensureIndexes } from '$lib/server/collections';

let indexesEnsured = false;

export const handle: Handle = async ({ event, resolve }) => {
  if (!indexesEnsured) {
    await ensureIndexes();
    indexesEnsured = true;
  }

  const { pathname } = event.url;

  // Public routes
  if (pathname === '/login') {
    return resolve(event);
  }

  // API routes: check X-API-Key header
  if (pathname.startsWith('/api/')) {
    const apiKey = event.request.headers.get('X-API-Key');
    if (!apiKey || apiKey !== env.API_KEY) {
      return new Response('Unauthorized', { status: 401 });
    }
    return resolve(event);
  }

  // All other routes: check session cookie
  const sessionKey = event.cookies.get('session');
  if (!sessionKey || sessionKey !== env.API_KEY) {
    throw redirect(303, '/login');
  }

  return resolve(event);
};
