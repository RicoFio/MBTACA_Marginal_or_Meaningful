<script>
	export let activeSelection;
	
	// Function to determine if the current label should be highlighted
	function isSelected(value) {
	  return activeSelection === value ? 'selected' : '';
	}
  </script>
  
  <div class="radio-container">
	<div class="row-radio-container">
	  {#each ['age', 'race', 'gender', 'median household income'] as category}
	  <label class={isSelected(category)}>
		<input type="radio" bind:group={activeSelection} name="selector" value={category}>
		{category.replace(/_/g, ' ').toUpperCase()} <!-- Improved readability -->
	  </label>
	  {/each}
	</div>
	<div class="row">
	  {#each ['vehicles per household', 'mode of transportation'] as category}
	  <label class={isSelected(category)}>
		<input type="radio" bind:group={activeSelection} name="selector" value={category}>
		{category.replace(/_/g, ' ').toUpperCase()} <!-- Improved readability -->
	  </label>
	  {/each}
	</div>
  </div>
  
  <style>
	.radio-container {
	  display: flex;
	  flex-direction: column; /* Align items in columns for two rows */
	  gap: 10px; /* Space between rows */
	  padding: 4px;
	  border-radius: 2px;
	  align-items: center; /* Align the entire container's content in the center */
	}
  
	.row-radio-container {
	  display: flex;
	  flex-direction: row;
	  gap: 10px;
	  justify-content: center; /* Center-align the items within each row */
	}
  
	label {
	  cursor: pointer;
	  transition: background-color 0.3s ease, color 0.3s ease;
	  padding: 5px 10px; /* Padding for better touch area */
	  border-radius: 4px; /* Rounded corners */
	  white-space: nowrap;
	}

	label:hover {
		background-color: #f0f0f0; /* Light grey background on hover */
		color: #333; /* Darker text on hover */
	}
  
	input[type="radio"] {
	  display: none;
	}
  
	.selected {
	  font-weight: bold;
	  background-color: #dedede; /* Light grey background for selected item */
	}
  </style>
  
  