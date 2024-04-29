<script>
	export let activeSelection;
	
	// Function to determine if the current label should be highlighted
	function isSelected(value) {
		return activeSelection === value ? 'selected' : '';
	}
	</script>
	
	<div class="radio-container">
		{#each ['age', 'race', 'gender', 'mean household income', 'vehicles per household', 'mode of transportation'] as category}
		<label class={isSelected(category)}>
			<input type="radio" bind:group={activeSelection} name="selector" value={category}>
			{category.replace(/_/g, ' ').toUpperCase()} <!-- Improved readability -->
		</label>
		{/each}
	</div>
	
	<style>
		.radio-container {
			position: relative;
			top: 16px;
			left: 16px;
			padding: 4px;
			border-radius: 2px;
			display: flex;
			flex-direction: row; /* Align items horizontally */
			gap: 10px; /* Add some space between items */
		}
	
		/* Basic styling for labels */
		label {
			cursor: pointer;
			transition: font-weight 0.3s ease;
			white-space: nowrap; /* Prevent labels from wrapping */
		}
	
		/* Hide the radio button */
		input[type="radio"] {
			display: none;
		}
	
		/* When a label is selected, make the text bold */
		.selected {
			font-weight: bold;
		}
	</style>
	