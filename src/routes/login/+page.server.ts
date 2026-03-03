import { fail, redirect } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
import type { Actions } from './$types';

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const password = data.get('password');

    if (!password || password !== env.API_KEY) {
      return fail(401, { error: 'Invalid password' });
    }

    cookies.set('session', env.API_KEY, {
      path: '/',
      httpOnly: true,
      sameSite: 'strict',
      maxAge: 60 * 60 * 24 * 7 // 1 week
    });

    throw redirect(303, '/week');
  }
};
