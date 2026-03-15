<script lang="ts">
	import { getPrevWeekOf, getNextWeekOf, formatWeekRange } from '$lib/week';

	let {
		weekOf,
		onNavigate
	}: {
		weekOf: string;
		onNavigate: (newWeekOf: string) => void;
	} = $props();
</script>

<div class="flex items-center justify-between gap-2">
	<button
		type="button"
		onclick={() => onNavigate(getPrevWeekOf(weekOf))}
		class="rounded-lg px-3 py-1.5 text-xs font-mono font-semibold text-stone-500 bg-stone-100 hover:bg-stone-200 hover:text-stone-700 transition-colors"
	>
		← Prev
	</button>
	<span class="text-xs font-mono text-stone-500">{formatWeekRange(weekOf)}</span>
	<button
		type="button"
		onclick={() => onNavigate(getNextWeekOf(weekOf))}
		class="rounded-lg px-3 py-1.5 text-xs font-mono font-semibold text-stone-500 bg-stone-100 hover:bg-stone-200 hover:text-stone-700 transition-colors"
	>
		Next →
	</button>
</div>
