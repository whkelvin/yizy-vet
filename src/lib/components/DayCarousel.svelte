<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/state';

	let {
		weekDates,
		selectedDate
	}: {
		weekDates: string[];
		selectedDate: string;
	} = $props();

	const DAY_LABELS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

	function dayLabel(dateStr: string): string {
		const d = new Date(dateStr + 'T00:00:00Z');
		return DAY_LABELS[d.getUTCDay()];
	}

	function dayNum(dateStr: string): string {
		const d = new Date(dateStr + 'T00:00:00Z');
		return String(d.getUTCDate());
	}

	function navigate(date: string) {
		const url = new URL(page.url);
		url.searchParams.set('date', date);
		goto(url.toString());
	}
</script>

<div class="flex gap-1 overflow-x-auto pb-1">
	{#each weekDates as date}
		<button
			type="button"
			onclick={() => navigate(date)}
			class="flex flex-col items-center rounded-lg px-3 py-2 min-w-[48px] transition-colors
				{date === selectedDate
				? 'bg-stone-800 text-white'
				: 'bg-stone-100 text-stone-500 hover:bg-stone-200 hover:text-stone-700'}"
		>
			<span class="text-[10px] font-semibold uppercase tracking-wide">{dayLabel(date)}</span>
			<span class="text-sm font-bold">{dayNum(date)}</span>
		</button>
	{/each}
</div>
