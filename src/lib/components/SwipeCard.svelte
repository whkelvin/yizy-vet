<script lang="ts">
	import type { Entry } from '$lib/types';
	import EntryCard from './EntryCard.svelte';

	let {
		entry,
		onswipe,
		onskip
	}: {
		entry: Entry;
		onswipe: (id: string, status: 'kept' | 'rejected') => void;
		onskip: (id: string) => void;
	} = $props();

	let THRESHOLD = $state(80);
	$effect(() => {
		THRESHOLD = Math.min(80, window.innerWidth * 0.15);
	});

	let startX = $state(0);
	let startY = $state(0);
	let dx = $state(0);
	let dragging = $state(false);
	let directionLocked = $state<'horizontal' | 'vertical' | null>(null);
	let touchTarget: EventTarget | null = null;
	let dismissed = $state(false);
	let dismissDir = $state<'kept' | 'rejected' | null>(null);
	let cardEl: HTMLElement;

	const LOCK_THRESHOLD = 6;

	let rotation = $derived(dx * 0.08);
	let opacity = $derived(dismissed ? 0 : 1);

	function handleStart(clientX: number, clientY: number, target: EventTarget | null) {
		if (dismissed) return;
		dragging = true;
		directionLocked = null;
		startX = clientX;
		startY = clientY;
		touchTarget = target;
	}

	function handleMove(clientX: number, clientY: number, preventDefault: () => void) {
		if (!dragging || dismissed) return;

		if (!directionLocked) {
			const absDx = Math.abs(clientX - startX);
			const absDy = Math.abs(clientY - startY);
			if (absDx < LOCK_THRESHOLD && absDy < LOCK_THRESHOLD) return;
			directionLocked = absDy > absDx * 2 ? 'vertical' : 'horizontal';
		}

		if (directionLocked === 'vertical') {
			// Let the browser handle native scrolling
			return;
		}

		// Horizontal swipe — prevent browser scroll and update dx
		preventDefault();
		dx = clientX - startX;
	}

	function handleEnd() {
		if (!dragging) return;
		dragging = false;

		if (Math.abs(dx) >= THRESHOLD) {
			dismissDir = dx > 0 ? 'kept' : 'rejected';
			dismissed = true;
			setTimeout(() => {
				onswipe(entry._id, dismissDir!);
			}, 300);
		} else {
			dx = 0;
		}
	}

	// Touch events for mobile
	function ontouchstart(e: TouchEvent) {
		const t = e.touches[0];
		handleStart(t.clientX, t.clientY, e.target);
	}

	function ontouchmove(e: TouchEvent) {
		const t = e.touches[0];
		handleMove(t.clientX, t.clientY, () => e.preventDefault());
	}

	function ontouchend() {
		handleEnd();
	}

	// Mouse events for desktop
	function onmousedown(e: MouseEvent) {
		handleStart(e.clientX, e.clientY, e.target);
		// Listen on window so drag works outside the card
		window.addEventListener('mousemove', onmousemove);
		window.addEventListener('mouseup', onmouseup);
	}

	function onmousemove(e: MouseEvent) {
		handleMove(e.clientX, e.clientY, () => e.preventDefault());
	}

	function onmouseup() {
		handleEnd();
		window.removeEventListener('mousemove', onmousemove);
		window.removeEventListener('mouseup', onmouseup);
	}

	let translateX = $derived(dismissed ? (dismissDir === 'kept' ? 500 : -500) : dx);

	let indicatorKept = $derived(dx > 30);
	let indicatorReject = $derived(dx < -30);
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
	bind:this={cardEl}
	class="absolute inset-0 select-none cursor-grab active:cursor-grabbing"
	style="
		transform: translateX({translateX}px) rotate({rotation}deg);
		transition: {dismissed ? 'transform 0.3s ease, opacity 0.3s ease' : dragging ? 'none' : 'transform 0.2s ease'};
		opacity: {opacity};
		touch-action: pan-y;
	"
	onmousedown={onmousedown}
	ontouchstart={ontouchstart}
	ontouchmove={ontouchmove}
	ontouchend={ontouchend}
	ontouchcancel={ontouchend}
>
	<!-- Card body -->
	<div class="h-full rounded-2xl bg-white border border-stone-200 shadow-lg flex flex-col" class:dragging>
		<!-- Keep / Reject indicators -->
		{#if indicatorKept}
			<div class="absolute top-4 left-4 z-10 rounded-full border-2 border-green-500 px-3 py-1 text-xs font-bold text-green-500 uppercase tracking-wider rotate-[-15deg] opacity-{Math.min(100, Math.round((dx / THRESHOLD) * 100))}">
				Keep
			</div>
		{/if}
		{#if indicatorReject}
			<div class="absolute top-4 right-4 z-10 rounded-full border-2 border-red-500 px-3 py-1 text-xs font-bold text-red-500 uppercase tracking-wider rotate-[15deg] opacity-{Math.min(100, Math.round((Math.abs(dx) / THRESHOLD) * 100))}">
				Skip
			</div>
		{/if}

		<div class="flex-1 min-h-0 overflow-auto">
			<EntryCard {entry} />
		</div>

		<!-- Skip button -->
		<div class="shrink-0 p-3 border-t border-stone-200">
			<button
				class="w-full py-2 rounded-lg border border-stone-300 text-sm font-mono text-stone-500 hover:bg-stone-100 active:bg-stone-200 transition-colors"
				onclick={() => onskip(entry._id)}
			>
				Skip
			</button>
		</div>
	</div>
</div>

<style>
	.dragging :global(iframe) {
		pointer-events: none;
	}
</style>
