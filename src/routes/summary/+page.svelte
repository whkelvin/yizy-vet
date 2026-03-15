<script lang="ts">
	import { goto, invalidateAll } from '$app/navigation';
	import { page } from '$app/state';
	import type { Entry, WeeklyMeta, Edition } from '$lib/types';
	import RadioGroup from '$lib/components/RadioGroup.svelte';
	import WeekSummaryList from '$lib/components/WeekSummaryList.svelte';
	import WeekNavigator from '$lib/components/WeekNavigator.svelte';

	let {
		data
	}: {
		data: { weekOf: string; entries: Entry[]; meta: WeeklyMeta };
	} = $props();

	const STATUS_OPTIONS = [
		{ value: 'kept', label: 'Approved' },
		{ value: 'pending', label: 'Pending' },
		{ value: 'rejected', label: 'Rejected' }
	];

	// Local state that drives both RadioGroup display and entry filter
	let selectedStatus = $state(page.url.searchParams.get('status') ?? 'kept');
	let filteredEntries = $derived(data.entries.filter((e) => e.status === selectedStatus));

	// Sync state → URL whenever selectedStatus changes
	$effect(() => {
		const s = selectedStatus;
		const current = page.url.searchParams.get('status') ?? 'kept';
		if (s !== current) {
			goto(`?status=${s}`, { replaceState: true });
		}
	});

	function navigateWeek(newWeekOf: string) {
		goto(`/summary?weekOf=${newWeekOf}`);
	}

	// Date helpers
	let weekEnd = $derived.by(() => {
		const d = new Date(data.weekOf + 'T00:00:00Z');
		d.setUTCDate(d.getUTCDate() + 6);
		return d.toISOString().slice(0, 10);
	});

	let publishDate = $derived.by(() => {
		const d = new Date(data.weekOf + 'T00:00:00Z');
		d.setUTCDate(d.getUTCDate() + 7);
		return d.toISOString().slice(0, 10);
	});

	// Export
	let copyLabel = $state('Export JSON');
	let copyTimer: ReturnType<typeof setTimeout>;

	function buildEdition(): Edition {
		const kept = data.entries.filter((e) => e.status === 'kept');
		return {
			date: publishDate,
			articles: kept
				.filter((e) => e.kind === 'article')
				.map((e) => ({ title: e.title, url: e.url, why: e.why ?? '', description: e.description ?? '', kelvinsPick: e.kelvinsPick })),
			repos: kept
				.filter((e) => e.kind === 'repo')
				.sort((a, b) => (b.starsThisWeek ?? 0) - (a.starsThisWeek ?? 0))
				.slice(0, 10)
				.map((e) => ({
					name: e.repoName || e.title,
					url: e.url,
					starsThisWeek: e.starsThisWeek ?? 0,
					kelvinsPick: e.kelvinsPick
				})),
			videos: kept
				.filter((e) => e.kind === 'video')
				.map((e) => ({
					title: e.title,
					youtubeId: e.youtubeId ?? '',
					why: e.why ?? '',
					description: e.description ?? '',
					kelvinsPick: e.kelvinsPick
				})),
			podcasts: kept
				.filter((e) => e.kind === 'podcast')
				.map((e) => ({
					title: e.title,
					spotifyEmbedUrl: e.spotifyEmbedUrl ?? '',
					why: e.why ?? '',
					description: e.description ?? '',
					kelvinsPick: e.kelvinsPick
				})),
			kelvinsPick: data.meta?.kelvinsPick ?? { title: '', url: '', description: '' }
		};
	}

	async function handleExport() {
		const edition = buildEdition();
		await navigator.clipboard.writeText(JSON.stringify(edition, null, 2));
		clearTimeout(copyTimer);
		copyLabel = 'Copied!';
		copyTimer = setTimeout(() => {
			copyLabel = 'Export JSON';
		}, 2000);
	}

	// Kelvin's Pick
	let showPickForm = $state(false);
	let pickTitle = $state('');
	let pickUrl = $state('');
	let pickDescription = $state('');
	let pickSaving = $state(false);
	let pickError = $state('');

	// Sync pick display from server data (don't reset form fields)
	let localPick = $derived(data.meta?.kelvinsPick ?? null);

	async function savePick() {
		pickSaving = true;
		pickError = '';
		try {
			const res = await fetch('/api/weekly/pick', {
				method: 'PATCH',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					weekOf: data.weekOf,
					title: pickTitle,
					url: pickUrl,
					description: pickDescription
				})
			});
			if (!res.ok) throw new Error(await res.text());
			await invalidateAll();
			showPickForm = false;
		} catch (e) {
			pickError = e instanceof Error ? e.message : 'Failed to save';
		} finally {
			pickSaving = false;
		}
	}
</script>

<div class="min-h-screen bg-stone-200 px-4 py-6 flex flex-col gap-5 max-w-2xl mx-auto">
	<!-- Header -->
	<header class="flex items-center justify-between">
		<div>
			<h1 class="section-heading text-stone-700 mb-0">Week Summary</h1>
			<p class="text-xs font-mono text-stone-400 mt-1">{data.weekOf} — {weekEnd}</p>
		</div>
		<button
			onclick={handleExport}
			class="px-3 py-1.5 rounded-lg bg-stone-800 text-stone-100 text-xs font-mono font-semibold hover:bg-stone-700 transition-colors"
		>
			{copyLabel}
		</button>
	</header>

	<!-- Week Navigator -->
	<WeekNavigator weekOf={data.weekOf} onNavigate={navigateWeek} />

	<!-- Status filter -->
	<RadioGroup options={STATUS_OPTIONS} bind:selected={selectedStatus} />

	<!-- Entry count -->
	<p class="text-xs font-mono text-stone-400 -mt-2">{filteredEntries.length} entries</p>

	<!-- Entry list (non-repo) -->
	<WeekSummaryList entries={filteredEntries} kinds={['article', 'video', 'podcast']} />

	<!-- Kelvin's Pick -->
	<section class="mt-2">
		<h2 class="section-heading">Kelvin's Pick</h2>

		{#if !showPickForm}
			<div class="flex items-start justify-between gap-4 rounded-xl bg-white border border-stone-200 p-4">
				{#if localPick}
					<div class="flex-1 min-w-0">
						<a
							href={localPick.url}
							target="_blank"
							rel="noopener noreferrer"
							class="yizy-title text-sm hover:text-stone-900 line-clamp-1 block"
						>
							{localPick.title}
						</a>
						{#if localPick.description}
							<p class="yizy-description text-xs mt-1 line-clamp-2">{localPick.description}</p>
						{/if}
					</div>
				{:else}
					<p class="yizy-description text-sm italic">Not set</p>
				{/if}
				<button
					onclick={() => {
						pickTitle = localPick?.title ?? '';
						pickUrl = localPick?.url ?? '';
						pickDescription = localPick?.description ?? '';
						showPickForm = true;
					}}
					class="shrink-0 px-2.5 py-1 rounded-lg bg-stone-100 border border-stone-200 text-xs font-mono font-semibold text-stone-600 hover:bg-stone-200 transition-colors"
				>
					Set Pick
				</button>
			</div>
		{:else}
			<form
				onsubmit={(e) => {
					e.preventDefault();
					savePick();
				}}
				class="rounded-xl bg-white border border-stone-200 p-4 flex flex-col gap-3"
			>
				<input
					type="text"
					placeholder="Title"
					bind:value={pickTitle}
					required
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs font-mono bg-stone-50 focus:outline-none focus:border-stone-400"
				/>
				<input
					type="text"
					placeholder="URL"
					bind:value={pickUrl}
					required
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs font-mono bg-stone-50 focus:outline-none focus:border-stone-400"
				/>
				<textarea
					placeholder="Description"
					bind:value={pickDescription}
					rows={2}
					class="w-full px-3 py-2 rounded-lg border border-stone-200 text-xs font-mono bg-stone-50 focus:outline-none focus:border-stone-400 resize-none"
				></textarea>
				{#if pickError}
					<p class="text-xs font-mono text-red-500">{pickError}</p>
				{/if}
				<div class="flex gap-2 justify-end">
					<button
						type="button"
						onclick={() => (showPickForm = false)}
						class="px-3 py-1.5 rounded-lg text-xs font-mono font-semibold text-stone-500 hover:text-stone-700 transition-colors"
					>
						Cancel
					</button>
					<button
						type="submit"
						disabled={pickSaving}
						class="px-3 py-1.5 rounded-lg bg-stone-800 text-stone-100 text-xs font-mono font-semibold hover:bg-stone-700 transition-colors disabled:opacity-50"
					>
						{pickSaving ? 'Saving…' : 'Save'}
					</button>
				</div>
			</form>
		{/if}
	</section>

	<!-- Repos -->
	<WeekSummaryList entries={filteredEntries} kinds={['repo']} />
</div>
