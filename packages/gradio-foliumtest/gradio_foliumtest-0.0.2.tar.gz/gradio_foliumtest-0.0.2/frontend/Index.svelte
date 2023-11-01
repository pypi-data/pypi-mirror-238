<script lang="ts">

	import type { Gradio } from "@gradio/utils";
	import { Block, Empty, BlockLabel } from "@gradio/atoms";
	import { Plot, File } from "@gradio/icons";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import type { FileData } from "@gradio/client";
	import { normalise_file } from "@gradio/client";

	// General Block Props
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: FileData | null;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus;
	export let label: string | null;

	// Props for handling files
	export let root: string;
	export let proxy_url: string;

	export let height: number = 500;
	
	export let gradio: Gradio<{
		change: never;
	}>;

	let new_value: FileData | null;

	$: new_value = normalise_file(value, root, proxy_url);
	let old_value = new_value;

	$: if (JSON.stringify(new_value) !== JSON.stringify(old_value)) {
		gradio.dispatch("change");
		old_value = new_value;
	}

</script>

<Block {visible} {elem_id} {elem_classes} {container} {scale} {min_width}>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
		/>
	{/if}
	<BlockLabel show_label={true} Icon={Plot} label={label || "Folium Map"} />
	{#if value}
		<iframe src={new_value.url} title={label ?? "Folium Map"} height="{height}px"></iframe>
	{:else}
		<Empty unpadded_box={true} size="large"><Plot /></Empty>
	{/if}

</Block>

<style>
	iframe	 {
		display: flex;
		width: var(--size-full);
	}
</style>

