<script lang="ts">
	import { invalidateAll } from '$app/navigation';
	import type { Entry } from '$lib/types';
	import SwipeCard from './SwipeCard.svelte';

	let { entries }: { entries: Entry[] } = $props();

	// Only show pending entries
	let pending = $derived(entries.filter((e) => e.status === 'pending'));
	let queue = $state<Entry[]>([]);

	$effect(() => {
		queue = [...pending];
	});

	// Show top 3 cards for stacking effect
	let visibleCards = $derived(queue.slice(0, 3));

	async function handleSwipe(id: string, status: 'kept' | 'rejected') {
		// Remove from local queue immediately
		queue = queue.filter((e) => e._id !== id);

		try {
			await fetch(`/api/entries/${id}`, {
				method: 'PATCH',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ status })
			});
			await invalidateAll();
		} catch (err) {
			console.error('Failed to update entry:', err);
		}
	}
</script>

<div class="flex flex-col items-center gap-4 w-full">
	<!-- Card stack -->
	<div class="relative w-full max-w-sm" style="height: 480px;">
		{#if queue.length === 0}
			<div class="flex h-full items-center justify-center rounded-2xl border border-dashed border-stone-300 text-stone-400">
				<div class="text-center">
					<div class="text-2xl mb-2">✓</div>
					<p class="text-sm font-mono">All done for today</p>
				</div>
			</div>
		{:else}
			{#each visibleCards.slice().reverse() as entry, revIdx}
				{@const idx = visibleCards.length - 1 - revIdx}
				{@const isTop = idx === 0}
				<div
					class="absolute inset-0"
					style="
						transform: translateY({idx * 8}px) scale({1 - idx * 0.03});
						z-index: {visibleCards.length - idx};
						pointer-events: {isTop ? 'auto' : 'none'};
					"
				>
					{#if isTop}
						<SwipeCard {entry} onswipe={handleSwipe} />
					{:else}
						<div class="h-full rounded-2xl bg-white border border-stone-200 shadow"></div>
					{/if}
				</div>
			{/each}
		{/if}
	</div>

	<!-- Progress dots -->
	{#if pending.length > 0}
		<div class="flex items-center gap-1.5">
			{#each pending as entry, i}
				<div
					class="rounded-full transition-all {queue.some((q) => q._id === entry._id)
						? i === 0 || queue[0]._id === entry._id ? 'w-2 h-2 bg-stone-800' : 'w-1.5 h-1.5 bg-stone-400'
						: 'w-1.5 h-1.5 bg-stone-200'}"
				></div>
			{/each}
		</div>
		<p class="text-xs text-stone-400 font-mono">{queue.length} remaining</p>
	{/if}
</div>
