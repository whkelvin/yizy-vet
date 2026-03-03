<script lang="ts">
	import { enhance } from '$app/forms';
	import '../../app.css';

	let { form } = $props();
</script>

<svelte:head>
	<title>Login — Kelvin's Weekly Vet</title>
</svelte:head>

<div class="min-h-screen bg-stone-200 flex items-center justify-center p-4">
	<div class="w-full max-w-sm bg-stone-100 border border-stone-300 rounded-lg p-8 shadow-sm">
		<h1 class="yizy-title text-lg mb-1">Kelvin's Weekly</h1>
		<p class="yizy-description text-xs mb-6">vet dashboard</p>

		<form method="POST" use:enhance>
			<label class="block mb-2">
				<span class="section-heading text-xs">Password</span>
				<input
					type="password"
					name="password"
					autofocus
					autocomplete="current-password"
					class="mt-2 w-full bg-stone-200 border border-stone-300 rounded px-3 py-2 text-sm text-stone-800 font-mono placeholder-stone-400 focus:outline-none focus:border-stone-500 focus:ring-1 focus:ring-stone-500"
					placeholder="enter password"
				/>
			</label>

			{#if form?.error}
				<p class="text-red-600 text-xs mt-2 font-mono">{form.error}</p>
			{/if}

			<button
				type="submit"
				class="mt-4 w-full bg-stone-800 text-stone-100 text-sm font-mono py-2 px-4 rounded hover:bg-stone-700 transition-colors"
			>
				Enter
			</button>
		</form>
	</div>
</div>
