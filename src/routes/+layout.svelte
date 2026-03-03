<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { page } from '$app/state';

	let { children } = $props();

	const navItems = [
		{ href: '/week', label: 'Week View', icon: '◈' },
		{ href: '/summary', label: 'Summary', icon: '◉' }
	];

	function isActive(href: string) {
		return page.url.pathname.startsWith(href);
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex h-screen bg-stone-200">
	<!-- Desktop sidebar -->
	<aside class="hidden md:flex flex-col w-52 bg-stone-900 text-stone-100 shrink-0">
		<!-- Logo -->
		<div class="px-4 py-5 border-b border-stone-700">
			<span class="text-xs font-mono font-bold tracking-widest uppercase text-stone-300">
				yizy · vet
			</span>
		</div>

		<!-- Nav items -->
		<nav class="flex-1 py-3 flex flex-col gap-0.5 px-2">
			{#each navItems as item}
				<a
					href={item.href}
					class="flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-mono font-semibold transition-colors
						{isActive(item.href)
						? 'bg-stone-700 text-stone-100'
						: 'text-stone-400 hover:text-stone-100 hover:bg-stone-800'}"
				>
					<span class="text-base leading-none">{item.icon}</span>
					{item.label}
				</a>
			{/each}
		</nav>

		<!-- Logout -->
		<div class="p-3 border-t border-stone-700">
			<form method="POST" action="/logout">
				<button
					type="submit"
					class="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-xs font-mono font-semibold text-stone-500 hover:text-stone-200 hover:bg-stone-800 transition-colors"
				>
					<span class="text-base leading-none">⎋</span>
					Logout
				</button>
			</form>
		</div>
	</aside>

	<!-- Main content -->
	<main class="flex-1 overflow-auto pb-16 md:pb-0">
		{@render children()}
	</main>

	<!-- Mobile bottom tab bar -->
	<nav class="md:hidden fixed bottom-0 left-0 right-0 bg-stone-900 border-t border-stone-700 flex">
		{#each navItems as item}
			<a
				href={item.href}
				class="flex-1 flex flex-col items-center justify-center py-3 gap-1 text-xs font-mono font-semibold transition-colors
					{isActive(item.href) ? 'text-stone-100' : 'text-stone-500'}"
			>
				<span class="text-base leading-none">{item.icon}</span>
				<span class="text-[10px]">{item.label}</span>
			</a>
		{/each}
		<form method="POST" action="/logout" class="flex-1">
			<button
				type="submit"
				class="w-full h-full flex flex-col items-center justify-center py-3 gap-1 text-xs font-mono font-semibold text-stone-500"
			>
				<span class="text-base leading-none">⎋</span>
				<span class="text-[10px]">Logout</span>
			</button>
		</form>
	</nav>
</div>
